import time
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from langchain_core.messages import HumanMessage
from app import graph, config

root = tk.Tk()
root.title("Bank AI Assistant")
root.geometry("900x700")

chat = ScrolledText(root, height=22, width=100)
chat.pack(padx=10, pady=10)

chat.insert(tk.END, "Банковский AI Assistant готов к работе.\n\n")
chat.configure(state="disabled")

entry = tk.Text(root, height=4)
entry.pack(fill="x", padx=10)

stats = tk.Label(
    root,
    justify="left",
    anchor="w",
    font=("Consolas",10)
)

stats.pack(fill="x", padx=10, pady=10)

def send():

    text = entry.get("1.0", tk.END).strip()

    if not text:
        return

    entry.delete("1.0", tk.END)

    chat.configure(state="normal")

    chat.insert(tk.END, f"Вы:\n{text}\n\n")

    chat.configure(state="disabled")

    start = time.perf_counter()

    result = graph.invoke(
        {
            "messages":[HumanMessage(content=text)],
            "solution":"",
            "detected_topic":None,
            "normalized_topic":None,
            "retrieved_docs":[],
            "rag_context":"",
            "total_calls":0
        },
        config=config
    )

    finish = time.perf_counter()

    answer = result["messages"][-1].content

    chat.configure(state="normal")

    chat.insert(tk.END,f"Бот:\n{answer}\n\n")

    chat.configure(state="disabled")

    stats.config(
        text=
f"""
Тема: {result.get("detected_topic")}

Нормализованная:
{result.get("normalized_topic")}

Документов:
{len(result.get("retrieved_docs",[]))}

Размер контекста:
{len(result.get("rag_context",""))} символов

Вызовов LLM:
{result.get("total_calls")}

Время:
{finish-start:.2f} сек
"""
    )

button = tk.Button(
    root,
    text="Отправить",
    command=send,
    height=2
)

button.pack(pady=10)

def enter(event):
    send()
    return "break"

entry.bind("<Control-Return>", enter)

root.mainloop()