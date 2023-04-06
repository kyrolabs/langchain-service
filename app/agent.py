""""Agent model."""

import qdrant_client
from dotenv import load_dotenv
from langchain import OpenAI
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Qdrant

load_dotenv()


class Agent:
    """Agent model."""

    qa: RetrievalQA

    def __init__(self):
        llm = OpenAI()
        embeddings = OpenAIEmbeddings(client=llm)
        client = qdrant_client.QdrantClient(url="http://localhost/qdrant")
        qdrant = Qdrant(
            client=client,
            collection_name="langchain-service",
            embedding_function=embeddings.embed_query,
        )
        retriever = qdrant.as_retriever()
        self.qa = RetrievalQA.from_llm(llm=llm, retriever=retriever)

    def run(self, query: str) -> str:
        """Run the agent on a query."""
        return self.qa.run(query)
