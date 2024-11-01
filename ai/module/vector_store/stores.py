from abc import ABC, abstractmethod
from typing import List
from urllib.parse import urlparse

import chromadb
from langchain_chroma import Chroma
from langchain_core.documents import Document


class VectorStore(ABC):
    @abstractmethod
    def add_multiple_documents(self, documents: List[Document]):
        pass

    @abstractmethod
    def delete_document(self, document_name: str) -> None:
        pass

    @abstractmethod
    def get_all_documents(self) -> List[str]:
        pass


class ChromaClientVectorStore(VectorStore, ABC):
    def __init__(self, url: str, embedding_function):
        """
        Create a Chroma-based vector store
        :param url: url of the Chroma server
        :param embedding_function: embedding function to use for the vector store
        """
        parsed_url = urlparse(url)
        self.host = parsed_url.hostname
        self.port = parsed_url.port
        self.client = chromadb.HttpClient(self.host, self.port)
        self.embedding_function = embedding_function

        # Create or get a collection. You might want to make the collection name configurable
        self.collection = self.client.get_or_create_collection(
            name="chroma_vector_store", embedding_function=embedding_function
        )

    def get_vector_store_metadata(self) -> List:
        """
        Get the metadata of the vector store
        """
        result = self.collection.get()
        return result["metadatas"]

    def get_vector_store_documents(self) -> List[str]:
        """
        Get the documents from the vector store
        """
        result = self.collection.get()
        return result["documents"]

    def add_multiple_documents(self, documents: List[Document]):
        """
        Add multiple documents to the vector store
        """
        # Assuming Document class has text, metadata, and some sort of ID
        ids = [
            f"{doc.metadata['source']}_{doc.metadata['location']}" for doc in documents
        ]
        texts = [
            doc.page_content for doc in documents
        ]  # Assuming page_content holds the text
        metadatas = [doc.metadata for doc in documents]

        self.collection.add(documents=texts, metadatas=metadatas, ids=ids)

    def _get_matching_document_ids(self, document_name: str) -> List[str]:
        """
        Get all the chunks id that comes from the document
        """
        result = self.collection.get(where={"source": document_name})
        return result["ids"]

    def delete_document(self, document_name: str) -> None:
        """
        Delete chunks from a certain document from the Chroma store
        """
        matching_ids = self._get_matching_document_ids(document_name)
        self.collection.delete(ids=matching_ids)

    def get_all_documents(self) -> List[str]:
        """
        Get all unique document sources from the chunks
        """
        result = self.collection.get()
        return list(
            set(
                metadata["source"]
                for metadata in result["metadatas"]
                if metadata and "source" in metadata
            )
        )

    def as_retriever(self, search_kwargs: dict):
        """
        Converts the vector store into a retriever.

        :param search_kwargs: Parameters for retrieval, such as number of results (`k`) or filters.
        :return: A retriever object.
        """
        return Chroma(
            client=self.client,
            collection_name="chroma_vector_store",
            embedding_function=self.embedding_function
        ).as_retriever(search_kwargs=search_kwargs)
