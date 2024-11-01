from typing import Any, List

from module.text_segmentor import TextSegmentor
from module.vector_store import VectorStore
from module.vector_store.folder import (add_vectors_single_document,
                                        remove_vectors_single_document)

class DataPipeline:
    def __init__(
        self,
        embedding_model: Any,
        text_segmentor: TextSegmentor,
        vector_store: VectorStore,
    ) -> None:
        """
        Create a RAG pipeline using various components
        :param document_folder: the folder that contains the document
        :param llm_model: large language model for semantic retriever
        :param embedding_model: embedding for semantic retriever
        :param text_segmentor: text segmenting strategy
        :param vector_store: text chunk store
        :param prompt_template: the prompt used for RAG
        :param keyword_retriever_builder: builder for keyword-based document retriever
        :param semantic_retriever_builder: builder for semantic-based document retriever
        :param build_vector_store: whether to rebuild vector store or to use existing ones
        """
        # Save the embedding model
        self.embedding = embedding_model

        # Save the text segmentor
        self.text_segmentor = text_segmentor

        # Save the vector store
        self.vector_store = vector_store

    def add_single_document(self, document_path: str):
        """
        Add single document to the vector store
        """
        add_vectors_single_document(document_path, self.text_segmentor, self.vector_store)

    def remove_single_document(self, document_path: str):
        """
        Remove single document from the vector store
        """
        remove_vectors_single_document(document_path, self.vector_store)

    def get_all_documents(self) -> List[str]:
        return self.vector_store.get_all_documents()