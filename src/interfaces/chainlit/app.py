from io import BytesIO
import chainlit as cl
from pathlib import Path
from langchain_core.messages import AIMessageChunk, HumanMessage
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from src.modules.speech.speech_to_text import SpeechToText
from src.modules.image.image_to_text import ImageToText
from src.graph.graph import create_workflow_graph
from src.settings import settings

graph_builder=create_workflow_graph()

speech_to_text = SpeechToText()
image_to_text = ImageToText()

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH= DATA_DIR /settings.SHORT_TERM_MEMORY_DB_PATH


@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set("thread_id", 1)

@cl.on_message
async def on_message(message: cl.Message):
    msg = cl.Message(content="")

    # Process any attached images
    content = message.content
    if message.elements:
        for elem in message.elements:
            if isinstance(elem, cl.Image):
                with open(elem.path, "rb") as f:
                    image_bytes = f.read()

                try:
                    description = await image_to_text.analyze_image(
                        image_bytes,
                        "Please describe what you see in this image in the context of our conversation.",
                    )
                    content += f"\n[Image Analysis: {description}]"
                except Exception as e:
                    cl.logger.warning(f"Failed to analyze image: {e}")

    thread_id = cl.user_session.get("thread_id")

    async with cl.Step(type="run"):
        async with AsyncSqliteSaver.from_conn_string(DB_PATH) as short_term_memory:
            graph = graph_builder.compile(checkpointer=short_term_memory)
            async for chunk in graph.astream(
                {"messages": [HumanMessage(content=content)]},
                {"configurable": {"thread_id": thread_id}},
                stream_mode="messages",
            ):
                if chunk[1]["langgraph_node"] == "conversation_node" and isinstance(chunk[0], AIMessageChunk):
                    await msg.stream_token(chunk[0].content)

            output_state = await graph.aget_state(config={"configurable": {"thread_id": thread_id}})

    if output_state.values.get("workflow") == "audio":
        response = output_state.values["messages"][-1].content
        audio_buffer = output_state.values["audio_buffer"]
        output_audio_el = cl.Audio(
            name="Audio",
            auto_play=True,
            mime="audio/mpeg3",
            content=audio_buffer,
        )
        await cl.Message(content=response, elements=[output_audio_el]).send()
    elif output_state.values.get("workflow") == "image":
        response = output_state.values["messages"][-1].content
        # image = cl.Image(path=output_state.values["image_path"], display="inline")
        # await cl.Message(content=response, elements=[image]).send()
        await cl.Message(content=response).send()
    else:
        await msg.send()

@cl.on_audio_chunk
async def on_audio_chunk(chunk: cl.InputAudioChunk):
    """Handle incoming audio chunks"""
    if chunk.isStart:
        buffer = BytesIO()
        buffer.name = f"input_audio.{chunk.mimeType.split('/')[1]}"
        cl.user_session.set("audio_buffer", buffer)
        cl.user_session.set("audio_mime_type", chunk.mimeType)
    cl.user_session.get("audio_buffer").write(chunk.data)

@cl.on_audio_end
async def on_audio_end(elements):
    """Process completed audio input"""
    # Get audio data
    audio_buffer = cl.user_session.get("audio_buffer")
    audio_buffer.seek(0)
    audio_data = audio_buffer.read()

    # Show user's audio message
    input_audio_el = cl.Audio(mime="audio/mpeg3", content=audio_data)
    await cl.Message(author="You", content="You Said: ", elements=[input_audio_el, *elements]).send()

    # Use global SpeechToText instance
    transcription = await speech_to_text.transcribe(audio_data)

    thread_id = cl.user_session.get("thread_id")

    async with AsyncSqliteSaver.from_conn_string(DB_PATH) as short_term_memory:
        graph = graph_builder.compile(checkpointer=short_term_memory)
        output_state = await graph.ainvoke(
            {"messages": [HumanMessage(content=transcription)]},
            {"configurable": {"thread_id": thread_id}},
        )

    # audio_buffer = await text_to_speech.synthesize(output_state["messages"][-1].content)

    # output_audio_el = cl.Audio(
    #     name="Audio",
    #     auto_play=True,
    #     mime="audio/mpeg3",
    #     content=audio_buffer,
    # )
    # await cl.Message(content=output_state["messages"][-1].content, elements=[output_audio_el]).send()

    response = output_state["messages"][-1].content
    if output_state.get("workflow") == "audio":
        audio_buffer = output_state.values["audio_buffer"]
        output_audio_el = cl.Audio(
            name="Audio",
            auto_play=True,
            mime="audio/mpeg3",
            content=audio_buffer,
        )
        await cl.Message(content=response, elements=[output_audio_el]).send()
    elif output_state.get("workflow") == "image":
        # image = cl.Image(path=output_state.values["image_path"], display="inline")
        # await cl.Message(content=response, elements=[image]).send()
        await cl.Message(content=response).send()
    else:
        await cl.Message(content=response).send()