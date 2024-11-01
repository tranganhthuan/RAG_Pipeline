from abc import ABC, abstractmethod

from langchain.schema import Document
from langchain.schema.runnable import RunnableLambda
from langchain_community.retrievers import BM25Retriever
from module.vector_store import VectorStore


class DocumentRetrieverBuilder(ABC):
    def __init__(self, k: int, vector_store: VectorStore):
        self.k = k
        self.vector_store = vector_store

    @abstractmethod
    def build(self):
        pass


class BM25RetrieverBuilder(DocumentRetrieverBuilder):
    def build(self):
        documents = self.vector_store.get_vector_store_documents()

        if len(documents) == 0:
            return RunnableLambda(lambda x: [Document(page_content="", metadata={"source": "", "location": ""})])

        metadatas = self.vector_store.get_vector_store_metadata()

        documents = [
            Document(
                page_content=documents[index],
                metadata={
                    "source": metadata["source"],
                    "location": metadata["location"],
                },
            )
            for index, metadata in enumerate(metadatas)
        ]

        # Initialize the retriever with Document objects
        return BM25Retriever.from_documents(documents, k=self.k)


class ChromaRetrieverBuilder(DocumentRetrieverBuilder):
    def build(self):
        documents = self.vector_store.get_vector_store_documents()

        if len(documents) == 0:
            return RunnableLambda(lambda x: [Document(page_content="", metadata={"source": "", "location": ""})])
        return self.vector_store.as_retriever(search_kwargs={"k": self.k})
