import customtkinter as ctk
from langchain_core.messages import HumanMessage
from app import graph
import uuid

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()

current_config = {
    "configurable": {
        "thread_id": str(uuid.uuid4())
    }
}

app.title("🤖 Bank AI Assistant")
app.geometry("1200x800")


header = ctk.CTkFrame(app, height=60)
header.pack(fill="x", padx=15, pady=10)

title = ctk.CTkLabel(
    header,
    text="🤖 Bank AI Assistant",
    font=("Segoe UI", 22, "bold")
)

title.pack(side="left", padx=20)

status = ctk.CTkLabel(
    header,
    text="🟢 Online",
    font=("Segoe UI", 15)
)

status.pack(side="right", padx=20)

main = ctk.CTkFrame(app)
main.pack(fill="both", expand=True, padx=15, pady=10)

chat = ctk.CTkTextbox(
    main,
    font=("Segoe UI",15),
    wrap="word"
)

chat.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=15
)

chat.insert("end","Банковский AI Assistant готов к работе.\n\n")
chat.configure(state="disabled")

bottom = ctk.CTkFrame(app,height=80)
bottom.pack(fill="x",padx=15,pady=10)

entry = ctk.CTkEntry(
    bottom,
    placeholder_text="Введите обращение...",
    height=45,
    font=("Segoe UI",15)
)

entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(15,10),
    pady=15
)


info = ctk.CTkFrame(main,width=260)
info.pack(side="right",fill="y",padx=10,pady=15)

topic_label = ctk.CTkLabel(
    info,
    text="Тема:\n-",
    anchor="w",
    justify="left",
    font=("Segoe UI",15)
)

topic_label.pack(fill="x",padx=15,pady=10)

docs_label = ctk.CTkLabel(
    info,
    text="Документов:\n0",
    anchor="w",
    justify="left",
    font=("Segoe UI",15)
)

docs_label.pack(fill="x",padx=15,pady=10)

context_label = ctk.CTkLabel(
    info,
    text="Контекст:\n0 символов",
    anchor="w",
    justify="left",
    font=("Segoe UI",15)
)

context_label.pack(fill="x",padx=15,pady=10)

calls_label = ctk.CTkLabel(
    info,
    text="LLM вызовов:\n0",
    anchor="w",
    justify="left",
    font=("Segoe UI",15)
)

calls_label.pack(fill="x",padx=15,pady=10)

time_label = ctk.CTkLabel(
    info,
    text="Время:\n0 сек",
    anchor="w",
    justify="left",
    font=("Segoe UI",15)
)

time_label.pack(fill="x",padx=15,pady=10)

import time
import threading

def update_stats(result, elapsed):

    topic_label.configure(
        text=f"Тема:\n{result.get('detected_topic')}"
    )

    docs_label.configure(
        text=f"Документов:\n{len(result.get('retrieved_docs', []))}"
    )

    context_label.configure(
        text=f"Контекст:\n{len(result.get('rag_context',''))} символов"
    )

    calls_label.configure(
        text=f"LLM вызовов:\n{result.get('total_calls')}"
    )

    time_label.configure(
        text=f"Время:\n{elapsed:.2f} сек"
    )

def send_message():

    text = entry.get().strip()

    if text == "":
        return

    entry.delete(0, "end")

    chat.configure(state="normal")

    chat.insert(
        "end",
        f"👤 Вы:\n{text}\n\n"
    )

    chat.insert(
        "end",
        "🤖 Думаю...\n\n"
    )

    chat.configure(state="disabled")
    chat.see("end")

    threading.Thread(
        target=run_graph,
        args=(text,),
        daemon=True
    ).start()

def run_graph(user_text):

    start = time.perf_counter()

    global current_config

    add_log("Запуск графа LangGraph")

    result = graph.invoke(
        {
            "messages":[
                HumanMessage(content=user_text)
            ],

            "solution":"",
            "detected_topic":None,
            "normalized_topic":None,
            "retrieved_docs":[],
            "rag_context":"",
            "total_calls":0

        },
        config=current_config
    )

    elapsed = time.perf_counter()-start

    add_log(
    f"Завершено за {elapsed:.2f} сек"
    )

    add_log(
        f"Тема: {result.get('detected_topic')}"
    )

    add_log(
        f"Документы: {len(result.get('retrieved_docs',[]))}"
    )

    add_log(
        f"LLM вызовы: {result.get('total_calls')}"
    )

    answer = result["messages"][-1].content

    app.after(
        0,
        lambda:update_chat(
            answer,
            result,
            elapsed
        )
    )

def update_chat(answer,result,elapsed):

    chat.configure(state="normal")

    chat.delete("end-3l","end")

    chat.insert(
        "end",
        f"🤖 Бот:\n{answer}\n\n"
    )

    chat.configure(state="disabled")

    chat.see("end")

    update_stats(result,elapsed)

send_btn = ctk.CTkButton(
    bottom,
    text="Отправить",
    width=140,
    height=45,
    command=send_message
)

send_btn.pack(
    side="right",
    padx=(0,15),
    pady=15
)

def new_dialog():

    global current_config

    current_config = {
        "configurable":{
            "thread_id":str(uuid.uuid4())
        }
    }


    chat.configure(state="normal")

    chat.delete(
        "1.0",
        "end"
    )


    chat.insert(
        "end",
        "🆕 Новый пользователь подключен\n\n"
        "Банковский AI Assistant готов к работе.\n\n"
    )


    chat.configure(state="disabled")


    topic_label.configure(
        text="Тема:\n-"
    )

    docs_label.configure(
        text="Документов:\n0"
    )

    context_label.configure(
        text="Контекст:\n0 символов"
    )

    calls_label.configure(
        text="LLM вызовов:\n0"
    )

    time_label.configure(
        text="Время:\n0 сек"
    )

logs = ctk.CTkTextbox(
    main,
    height=180,
    font=("Consolas",13),
    fg_color="#111111"
)

logs.pack(
    fill="x",
    padx=15,
    pady=(0,15)
)


logs.insert(
    "end",
    "=== SYSTEM LOG ===\n"
)

logs.configure(state="disabled")

def add_log(text):

    def update():

        logs.configure(state="normal")

        logs.insert(
            "end",
            f"{time.strftime('%H:%M:%S')} | {text}\n"
        )

        logs.configure(state="disabled")
        logs.see("end")


    app.after(0, update)

def start_test():

    threading.Thread(
        target=run_tests,
        daemon=True
    ).start()

def run_tests():

    with open(
        "tests/queries.txt",
        encoding="utf-8"
    ) as f:

        queries = f.readlines()


    add_log(
        f"Запуск теста: {len(queries)} запросов"
    )


    total_time = 0


    for i,q in enumerate(queries):

        q=q.strip()

        if not q:
            continue


        start=time.perf_counter()


        result=graph.invoke(
            {
                "messages":[
                    HumanMessage(content=q)
                ],
                "solution":"",
                "detected_topic":None,
                "normalized_topic":None,
                "retrieved_docs":[],
                "rag_context":"",
                "total_calls":0
            },
            config={
                "configurable":{
                    "thread_id":str(uuid.uuid4())
                }
            }
        )


        elapsed=time.perf_counter()-start

        total_time+=elapsed


        add_log(
            f"[{i+1}/{len(queries)}] "
            f"{elapsed:.2f}s | "
            f"topic={result.get('detected_topic')}"
        )


    avg=total_time/len(queries)


    add_log(
        f"Среднее время ответа: {avg:.2f} сек"
    )

    add_log(
        "Тестирование завершено"
    )

test_btn = ctk.CTkButton(
    bottom,
    text="🧪 Тест агента",
    width=140,
    height=45,
    command=start_test
)

test_btn.pack(
    side="right",
    padx=10
)





clear_btn = ctk.CTkButton(
    bottom,
    text="🧹 Очистить логи",
    command=lambda:clear_logs()
)

clear_btn.pack(
    side="right",
    padx=10
)

def clear_logs():

    logs.configure(state="normal")

    logs.delete(
        "1.0",
        "end"
    )

    logs.insert(
        "end",
        "=== SYSTEM LOG ===\n"
    )

    logs.configure(state="disabled")

new_btn = ctk.CTkButton(
    bottom,
    text="🆕 Новый диалог",
    width=160,
    height=45,
    command=new_dialog
)

new_btn.pack(
    side="right",
    padx=(0,10),
    pady=15
)

entry.bind(
    "<Return>",
    lambda event: send_message()
)

chat.insert(
    "end",
    "────────────────────────────────────\n"
)


app.mainloop()