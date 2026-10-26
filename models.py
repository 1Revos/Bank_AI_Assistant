from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

load_dotenv()

embeddings = HuggingFaceEmbeddings(
    model_name=
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)


llm = ChatOpenAI(
    model="gpt-6-luna",
    max_tokens=512
)