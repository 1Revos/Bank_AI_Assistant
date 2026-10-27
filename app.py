from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver


from src.state import State
from src.nodes import (
    detect_topic,
    retrieve_documents,
    generate_answer,
    generate_without_rag,
    check_topic_exists,
    check_documents,
    save_to_bd
)

builder = StateGraph(State)

# Добавляем все узлы логики агента
builder.add_node("detect_topic", detect_topic)
builder.add_node("retrieve_documents", retrieve_documents)
builder.add_node("generate_answer", generate_answer)
builder.add_node("generate_without_rag", generate_without_rag)
builder.add_node("save_to_bd", save_to_bd)


builder.add_edge(START, "detect_topic")

builder.add_conditional_edges(
    "detect_topic",
    check_topic_exists,
    {
        "retrieve_documents": "retrieve_documents",
        "generate_without_rag": "generate_without_rag"
    }
)

builder.add_conditional_edges(
    "retrieve_documents",
    check_documents,
    {
        "generate_answer": "generate_answer",
        "generate_without_rag": "generate_without_rag"
    }
)

builder.add_edge("generate_answer", "save_to_bd")
builder.add_edge("generate_without_rag", "save_to_bd")
builder.add_edge("save_to_bd", END)


checkpointer = MemorySaver()
graph = builder.compile(checkpointer=checkpointer)


config = {
    "configurable": {
        "thread_id": "default"
    }
}


if __name__ == "__main__":
    from src.ui.ui_ultra import app
    
    print("Инициализация графа успешна. Запуск Bank AI Assistant...")
    app.mainloop()


