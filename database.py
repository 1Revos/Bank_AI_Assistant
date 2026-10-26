from langchain_postgres import PGVector

from models import embeddings
from config import NEON_CONNECTION_STRING



topic_vector_store = PGVector(
    embeddings=embeddings,
    collection_name="topics",
    connection=NEON_CONNECTION_STRING,
    use_jsonb=True
)



knowledge_vector_store = PGVector(
    embeddings=embeddings,
    collection_name="support_knowledge_base",
    connection=NEON_CONNECTION_STRING,
    use_jsonb=True
)