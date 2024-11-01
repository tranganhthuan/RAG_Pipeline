"""
Author: Trang Anh Thuan & Son Phat Tran
This file contains the logic for the RAG pipeline
"""

from langchain import hub
from configs.config import VECTOR_STORE_URL
from module.document_retriever import BM25RetrieverBuilder, ChromaRetrieverBuilder
from module.llm import LargeLanguageModelBuilder
from module.text_segmentor import MarkDownHeaderSegmentor
from module.vector_store import ChromaClientVectorStore
from module.vector_store.embedding_functions import EmbeddingFunctionWrapper

from .data_pipeline import DataPipeline
from .rag_pipeline import RAGPipeline

# Create the LLMs and Embeddings using your API key
# Remember to replace with your Google Gemini API Key
embedding = LargeLanguageModelBuilder.get_google_gemini_embedding()
embedding_function = EmbeddingFunctionWrapper(embedding)

# Create the text segmentor
# More will be created in the future
segmentor = MarkDownHeaderSegmentor()

# Create a store for text chunks
# Replace with your appropriate folder
# text_store = JsonVectorStore("data/vectors/json/data.json")
vector_store = ChromaClientVectorStore(VECTOR_STORE_URL, embedding_function)

# Create prompt template
prompt = hub.pull("rlm/rag-prompt")

# Create BM25 keyword retriever and Chroma semantic retriever
keyword_builder = BM25RetrieverBuilder(k=1, vector_store=vector_store)
semantic_builder = ChromaRetrieverBuilder(k=1, vector_store=vector_store)

gemini_model = LargeLanguageModelBuilder.get_google_gemini_llm()
openai_model = LargeLanguageModelBuilder.get_open_ai_llm()
ollama_model = LargeLanguageModelBuilder.get_ollama_llm()

llm_models = {
    "gemini": gemini_model,
    "openai": openai_model,
    "ollama": ollama_model,
}

# Create RAG
rag_pipeline = RAGPipeline(
    llm_model=llm_models,
    prompt_template=prompt,
    keyword_retriever_builder=keyword_builder,
    semantic_retriever_builder=semantic_builder,
)
data_pipeline = DataPipeline(
    embedding_model=embedding_function,
    vector_store=vector_store,
    text_segmentor=segmentor,
)