"""Ingest Notion DB data to QDrant and process its embeddings."""

import os

import openai
from dotenv import load_dotenv
from langchain.document_loaders import NotionDBLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Qdrant

load_dotenv()

# from langchain.indexes import VectorstoreIndexCreator

# index = VectorstoreIndexCreator().from_loaders([loader])

NOTION_TOKEN = os.environ["NOTION_TOKEN"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
DATABASE_ID = os.environ["DATABASE_ID"]
QDRANT_API_KEY = os.environ["QDRANT_API_KEY"]


if __name__ == "__main__":
    openai.api_key = OPENAI_API_KEY
    embeddings = OpenAIEmbeddings(client=openai)
    loader = NotionDBLoader(NOTION_TOKEN, DATABASE_ID)
    docs = loader.load()
    doc_store = Qdrant.from_documents(
        docs, embeddings, host="localhost", path="/qdrant", api_key=QDRANT_API_KEY
    )
