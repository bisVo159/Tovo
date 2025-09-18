from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.graph.utils.helpers import get_chat_model, AsteriskRemovalParser
from src.core.prompts import ROUTER_PROMPT, CHARACTER_CARD_PROMPT
from pydantic import BaseModel, Field
from typing import Literal


class RouterResponse(BaseModel):
    response_type: Literal['conversation','image','audio'] = Field(...,
        description="The response type to give to the user. It must be one of: 'conversation', 'image' or 'audio'"
    )

def get_router_chain():
    model = get_chat_model(temperature=0.3).with_structured_output(RouterResponse)

    prompt = ChatPromptTemplate.from_messages(
        [("system", ROUTER_PROMPT), MessagesPlaceholder(variable_name="messages")]
    )

    return prompt | model

def get_character_response_chain(summary: str = ""):
    model = get_chat_model()
    system_message = CHARACTER_CARD_PROMPT

    if summary:
        system_message += f"\n\nSummary of conversation earlier between Tovo and the user: {summary}"

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_message),
            MessagesPlaceholder(variable_name="messages"),
        ]
    )

    return prompt | model | AsteriskRemovalParser()