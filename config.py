from dotenv import load_dotenv
import os


load_dotenv()


NEON_CONNECTION_STRING = os.getenv(
    "NEON_CONNECTION_STRING"
)