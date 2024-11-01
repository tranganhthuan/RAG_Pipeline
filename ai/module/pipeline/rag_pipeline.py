from typing import Any, Dict, List

from langchain.schema import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from module.document_retriever import DocumentRetrieverBuilder



class RAGAnswer:
    def __init__(
        self,
        answer,
        keyword_context,
        keyword_metadata,
        semantic_context,
        semantic_metadata,
    ):
        """
        This class represents the answer for the RAG
        :param answer
        :param keyword_context
        :param keyword_metadata
        :param semantic_context
        :param semantic_metadata
        """
        self.answer = answer
        self.keyword_context = keyword_context
        self.keyword_metadata = keyword_metadata
        self.semantic_context = semantic_context
        self.semantic_metadata = semantic_metadata


def combine_results(results: Dict) -> List:
    """
    Combine the results from two retrievers
    :param results: dictionary containing the results
    :return: combine result
    """
    return results["keyword"] + results["semantic"]


def format_documents(docs: List[Document]) -> str:
    """
    Format the documents by adding new lines between them
    :param docs: the document
    :return:
    """
    return "\n\n".join(doc.page_content for doc in docs)


class RAGPipeline:
    def __init__(
        self,
        llm_model: Dict[str, Any],
        prompt_template: Any,
        keyword_retriever_builder: DocumentRetrieverBuilder,
        semantic_retriever_builder: DocumentRetrieverBuilder,
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
        # Save the document folder
        self.prompt = prompt_template

        # Save LLMs and embeddings
        self.llm = llm_model

        # Build the keyword retriever
        self.keyword_retriever = keyword_retriever_builder.build()
        self.semantic_retriever = semantic_retriever_builder.build()
        self.parallel_retriever = RunnableParallel(
            {"keyword": self.keyword_retriever, "semantic": self.semantic_retriever}
        )

        # Create the pipeline
        self.pre_rag_chain = (
            {
                "context": self.parallel_retriever | combine_results | format_documents,
                "question": RunnablePassthrough(),
            }
            | prompt_template
        )

        self.post_rag_chain = StrOutputParser()
    
    def rag_chain(self, model_name: str) -> Any:
        return self.pre_rag_chain | self.llm[model_name] | self.post_rag_chain

    def invoke(self, question: str, model_name: str) -> RAGAnswer:
        # Find the relevant documents
        docs = self.parallel_retriever.invoke(question)

        # Separate context and metadata for each retriever
        semantic_docs = docs["semantic"]
        text_docs = docs["keyword"]
        # Format the semantic context and metadata
        semantic_context = "\n".join([doc.page_content for doc in semantic_docs])
        semantic_metadata = "\n".join(
            [
                f"{doc.metadata['source']} (Chunk: {doc.metadata['location']})"
                for doc in semantic_docs
            ]
        )

        # Format the keyword context and metadata
        keyword_context = "\n".join([doc.page_content for doc in text_docs])
        keyword_metadata = "\n".join(
            [
                f"{doc.metadata['source']} (Chunk: {doc.metadata['location']})"
                for doc in text_docs
            ]
        )

        # Get the answer from the chain
        answer = self.rag_chain(model_name).invoke(question)

        # Return
        return RAGAnswer(
            answer,
            keyword_context,
            keyword_metadata,
            semantic_context,
            semantic_metadata,
        )
    