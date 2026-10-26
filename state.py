from typing import Optional

from langgraph.graph import MessagesState
from langchain_core.documents import Document



class State(MessagesState):

    detected_topic: Optional[str]

    normalized_topic: Optional[str]

    rag_context: Optional[str]

    retrieved_docs: list[Document]

    solution: Optional[str]

    total_calls: int