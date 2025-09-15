from langgraph.graph import MessagesState

class AgentState(MessagesState):
    summary: str
    workflow: str
    audio_buffer: bytes
    image_path: str
    current_activity: str
    apply_activity: bool
    memory_context: str