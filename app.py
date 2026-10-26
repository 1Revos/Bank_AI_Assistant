from langgraph.graph import (
    StateGraph,
    START,
    END
)


from langgraph.checkpoint.memory import MemorySaver


from state import State


from nodes import (
    detect_topic,
    retrieve_documents,
    generate_answer,
    generate_without_rag,
    check_topic_exists,
    check_documents,
    save_to_bd
)



builder=StateGraph(State)



builder.add_node(
    "detect_topic",
    detect_topic
)


builder.add_node(
    "retrieve_documents",
    retrieve_documents
)


builder.add_node(
    "generate_answer",
    generate_answer
)


builder.add_node(
    "generate_without_rag",
    generate_without_rag
)


builder.add_node(
    "save_to_bd",
    save_to_bd
)




builder.add_edge(
    START,
    "detect_topic"
)



builder.add_conditional_edges(

    "detect_topic",

    check_topic_exists,

    {

        "retrieve_documents":
        "retrieve_documents",

        "generate_without_rag":
        "generate_without_rag"

    }

)



builder.add_conditional_edges(

    "retrieve_documents",

    check_documents,

    {

        "generate_answer":
        "generate_answer",

        "generate_without_rag":
        "generate_without_rag"

    }

)



builder.add_edge(
    "generate_answer",
    "save_to_bd"
)



builder.add_edge(
    "generate_without_rag",
    "save_to_bd"
)



builder.add_edge(
    "save_to_bd",
    END
)



checkpointer=MemorySaver()



graph=builder.compile(
    checkpointer=checkpointer
)



config={

"configurable":
    {

    "thread_id":
    "default"

    }

}




# import os
# import json
# from typing_extensions import TypedDict, Literal, Optional
# from langgraph.graph import StateGraph, START, END, MessagesState
# from IPython.display import Image, display

# from langchain_core.messages import HumanMessage, SystemMessage
# from langchain_openai import ChatOpenAI
# from dotenv import load_dotenv
# from promts import sys_messg1, sys_messg2, sys_messg3

# from langchain_postgres import PGVector
# from langchain_core.documents import Document
# from langchain_huggingface import HuggingFaceEndpointEmbeddings, HuggingFaceEndpoint, ChatHuggingFace
# from langchain_ollama import ChatOllama
# from langchain_huggingface import HuggingFaceEmbeddings



# load_dotenv()

# #Rag

# embeddings = HuggingFaceEmbeddings(
#     model="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# )


# # vector_store = PGVector(
# #     embeddings=embeddings,
# #     collection_name="support_knowledge_base",
# #     connection=os.getenv("NEON_CONNECTION_STRING"),
# #     use_jsonb=True
# # )

# topic_vector_store = PGVector(
#     embeddings=embeddings,
#     collection_name="topics",
#     connection=os.getenv("NEON_CONNECTION_STRING"),
#     use_jsonb=True,
# )

# knowledge_vector_store = PGVector(
#     embeddings=embeddings,
#     collection_name="support_knowledge_base",
#     connection=os.getenv("NEON_CONNECTION_STRING"),
#     use_jsonb=True,
# )

# sys_messg_topic = SystemMessage(content = sys_messg1)
# sys_messg_global = SystemMessage(content = sys_messg2)
# sys_messg_without_rag = SystemMessage(content = sys_messg3)

# llm = ChatOpenAI(
#                 model = "gpt-6-luna",
#                 max_tokens=512
#             )

# # llm = ChatOpenAI(
# #     model="gpt-4o-mini",
# #     base_url="https://azure.com",
# #     openai_api_key=os.getenv("GITHUB_TOKEN"),
# #     max_tokens=512,
# #     temperature=0.2
# # )

# # llm = ChatOllama(
# #     model="qwen2.5:3b",
# #     temperature=0.2
# # )

# # class State(MessagesState):
# #     solution: Optional[str]
# #     topic: Optional[str]
# #     total_calls: int

# class State(MessagesState):
#     detected_topic: Optional[str]
#     normalized_topic: Optional[str]
#     rag_context: Optional[str]
#     retrieved_docs: list[Document]
#     solution: Optional[str]
#     total_calls: int

# #Nods

# def detect_topic(state: State) -> dict:

#     response = llm.invoke([sys_messg_topic] + state["messages"])

#     data = json.loads(response.content)


#     return {
#         "messages": [response],
#         "detected_topic": data["topic"],
#         "total_calls": state["total_calls"] + 1
#         }

# def retrieve_topic(state: State) -> dict:

#     if state["detected_topic"] is None:
#         return {
#             "normalized_topic": None
#         }

#     docs = topic_vector_store.similarity_search(
#         query=state["detected_topic"],
#         k=1
#     )

#     if docs:
#         normalized_topic = docs[0].page_content
#     else:
#         normalized_topic = state["detected_topic"]

#     return {
#         "normalized_topic": normalized_topic
#     }

# def generate_answer(state: State) -> dict:

#     prompt = [

#     sys_messg_global,

#     SystemMessage(
#         content=f"""
#     Контекст из базы знаний:

#     {state.get("rag_context","")}

#     Используй этот контекст только если он действительно подходит.

#     Если он пустой или нерелевантный —
#     ответь самостоятельно.
#     """
#             )
#         ] + state["messages"]

#     response = llm.invoke(prompt)

#     return {
#         "messages": [response],
#         "solution": response.content
#     }

# def generate_without_rag(state: State) -> dict:

#     response = llm.invoke([sys_messg_without_rag] + state["messages"])
    
#     return {
#             "messages": [response],
#             "solution": response.content,
#             "detected_topic": state["detected_topic"], 
#             "total_calls": state["total_calls"]
#             }

# def retrieve_documents(state: State) -> dict:

#     docs = knowledge_vector_store.similarity_search(
#     query=state["messages"][0].content,
#     filter={
#         "topic": state["normalized_topic"]
#     },
#     k=5
# )

#     context = "\n\n".join(
#         doc.page_content
#         for doc in docs
#     )

#     return {
#         "retrieved_docs": docs,
#         "rag_context": context
#     }

# def check_documents(state: State) -> Literal["generate_answer", "generate_without_rag"]:

#     if state["retrieved_docs"]:
#         return "generate_answer"

#     return "generate_without_rag"

# def check_topic_exists(state: State):

#     topic = state["detected_topic"]

#     if not topic:
#         return "generate_without_rag"


#     docs = topic_vector_store.similarity_search(
#         query=topic,
#         k=1
#     )


#     if docs:
#         return "retrieve_documents"

#     return "generate_without_rag"

# #Change

# def check_topic_exists(state: State) -> Literal["generate_without_rag", "retrieve_documents"]:

#     topic = state["detected_topic"]

#     if not topic:
#         return "generate_without_rag"


#     docs = topic_vector_store.similarity_search(
#         query=topic,
#         k=1
#     )


#     if docs:
#         return "retrieve_documents"


#     return "generate_without_rag"



# def save_to_bd(state: State):

#     topic = (
#         state.get("normalized_topic")
#         or state.get("detected_topic")
#     )

#     if not topic:
#         return state

#     customer_message = state["messages"][0].content

#     solution = state.get("solution", "")

#     result = f"""
#             ТЕМА: {topic}

#             ЖАЛОБА КЛИЕНТА:
#             {customer_message}

#             РЕШЕНИЕ:
#             {solution}
#             """

#     doc = Document(
#         page_content=result,
#         metadata={
#             "topic": topic
#         }
#     )

#     knowledge_vector_store.add_documents([doc])

#     existing = topic_vector_store.similarity_search_with_score(
#     query=topic,
#     k=1
# )

#     if not existing or existing[0][1] > 0.2:

#         topic_vector_store.add_documents([

#             Document(
#                 page_content=topic
#             )

#         ])

#     return state




# builder = StateGraph(State)

# builder.add_node("detect_topic", detect_topic)
# builder.add_node("retrieve_topic", retrieve_topic)
# builder.add_node("retrieve_documents", retrieve_documents)
# builder.add_node("generate_answer", generate_answer)
# builder.add_node("generate_without_rag", generate_without_rag)
# builder.add_node("save_to_bd", save_to_bd)




# builder.add_edge(START, "detect_topic")
# builder.add_conditional_edges(
#     "detect_topic",
#     check_topic_exists,
#     {
#         "retrieve_documents": "retrieve_documents",
#         "generate_without_rag": "generate_without_rag",
#     },
# )
# builder.add_conditional_edges(
#     "retrieve_documents",
#     check_documents,
#     {
#         "generate_answer": "generate_answer",
#         "generate_without_rag": "generate_without_rag",
#     },
# )
# builder.add_edge("generate_answer","save_to_bd")
# builder.add_edge("generate_without_rag", "save_to_bd")
# builder.add_edge("save_to_bd",END)



# from langgraph.checkpoint.memory import MemorySaver
# checkpointer = MemorySaver()

# graph = builder.compile(checkpointer=checkpointer)


# config = {
#     "configurable": {
#         "thread_id": "Kazino_777"
#     }
# }

# # messages = [HumanMessage(content="Добрый день. Подскажите, какие сейчас актуальные процентные ставки по вкладам и можно ли сделать рефинансирование старого займа под более низкий процент?")]
# # messages = graph.invoke({
# #     "messages": messages,
# #     "solution": "",
# #     "detected_topic": None,
# #     "normalized_topic": None,
# #     "retrieved_docs": [],
# #     "rag_context": "",
# #     "total_calls": 0
# # }, config=config)

# # last_message = messages['messages'][-1]
# # last_message.pretty_print()

# # print("\n--- ВСЕ СООБЩЕНИЯ В ГРАФЕ ---")
# # for i, msg in enumerate(messages['messages']):
# #     print(f"[{i}] {type(msg).__name__}: {repr(msg.content)}")

# # print("\n--- ДРУГИЕ ПОЛЯ СОСТОЯНИЯ ---")
# # print("Topic:", messages.get('topic'))
# # print("Solution:", messages.get('solution'))
# # print("Total calls:", messages.get('total_calls'))