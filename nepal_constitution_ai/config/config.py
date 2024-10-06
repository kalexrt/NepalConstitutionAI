import os
from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    LANGSMITH_API_KEY: str
    PINECONE_API_KEY: str
    OPENAI_API_KEY: str
    GROQ_API_KEY: str
    JINA_API_KEY: str
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"
    JINA_EMBEDDING_MODEL: str = "jina-embeddings-v3"
    OPENAI_EMBEDDING_DIM: str = "1536"
    JINA_EMBEDDING_DIM: str = "768"
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    GROQ_MODEL: str = "llama3-8b-8192"
    VECTOR_DB: str = "pinecone"
    PINECONE_INDEX: str
    PINECONE_CLOUD: str = "aws"
    PINECONE_REGION: str = "us-east-1"
    TOP_K:int = 4
    FILE_PATH: str=" data/nepal_constitution_2072.pdf"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
os.environ["LANGCHAIN_TRACING_V2"]="true" # enables the tracing
os.environ["LANGCHAIN_ENDPOINT"]="https://api.smith.langchain.com"
os.environ["LANGCHAIN_API_KEY"]=settings.LANGSMITH_API_KEY
os.environ["LANGCHAIN_PROJECT"]="RAG-FINAL_PROJECT-PROD"
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
__all__ = ["settings"]