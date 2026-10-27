import json
from langchain_core.messages import SystemMessage
from langchain_core.documents import Document
from typing_extensions import Literal
from src.models import llm

from src.database import (
    topic_vector_store,
    knowledge_vector_store
)

from src.promts import (
    sys_messg1,
    sys_messg2,
    sys_messg3
)



sys_messg_topic = SystemMessage(content=sys_messg1)
sys_messg_global = SystemMessage(content=sys_messg2)
sys_messg_without_rag = SystemMessage(content=sys_messg3)



def detect_topic(state):

    response = llm.invoke([sys_messg_topic] + state["messages"])

    data=json.loads(response.content)

    return {
        "messages":[response],
        "detected_topic":data["topic"],
        "total_calls":state["total_calls"] + 1
    }



def retrieve_documents(state):

    docs = knowledge_vector_store.similarity_search(
        query = state["messages"][0].content,
        filter={"topic": state["detected_topic"]},
        k=5
    )

    context="\n\n".join(d.page_content for d in docs)

    return {
        "retrieved_docs":docs,
        "rag_context":context
    }




def generate_answer(state):

    prompt=[sys_messg_global,SystemMessage(content=f"""Контекст:{state.get("rag_context","")}Используй только если подходит.""")] + state["messages"]

    response=llm.invoke(prompt)

    return {
        "messages":[response],
        "solution":
        response.content
    }





def generate_without_rag(state):

    response=llm.invoke([sys_messg_without_rag] + state["messages"])

    return {
        "messages":[response],
        "solution":
        response.content
    }





def check_topic_exists(state):

    topic=state["detected_topic"]

    if not topic:
        return "generate_without_rag"

    docs=topic_vector_store.similarity_search(
        topic,
        k=1
    )

    if docs:
        return "retrieve_documents"

    return "generate_without_rag"





def check_documents(state):

    if state["retrieved_docs"]:
        return "generate_answer"

    return "generate_without_rag"






def save_to_bd(state):

    topic = (state.get("detected_topic"))

    if not topic:
        return state

    result=f"""ТЕМА:{topic} ЖАЛОБА:{state["messages"][0].content} РЕШЕНИЕ:{state.get("solution","")}"""
    doc=Document(page_content=result,metadata={"topic":topic})

    knowledge_vector_store.add_documents([doc])

    topic_vector_store.add_documents([Document(page_content=topic)])

    return state