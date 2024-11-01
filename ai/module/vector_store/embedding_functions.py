"""
Author: Trang Anh Thuan & Son Phat Tran
This document creates custom embedding function wrappers for different LLMs
"""
from chromadb import Documents, EmbeddingFunction, Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings


class EmbeddingFunctionWrapper(EmbeddingFunction):
    """Base class for custom embedding functions"""
    def __init__(self, embedding_model: GoogleGenerativeAIEmbeddings | OpenAIEmbeddings | OllamaEmbeddings):
        """
        Initialize with any LangChain compatible embedding model
        :param embedding_model: LangChain embedding model instance
        """
        self.embeddings = embedding_model

    def __call__(self, input: Documents) -> Embeddings:
        """
        Generate embeddings for input documents
        :param input: List of text documents
        :return: List of embeddings
        """
        if isinstance(input, str):
            input = [input]
        return self.embeddings.embed_documents(input)
    
    def embed_query(self, text: str) -> Embeddings:
        """
        Generate embedding for a single query text
        :param text: Query text to embed
        :return: Embedding vector
        """
        return self.embeddings.embed_query(text)