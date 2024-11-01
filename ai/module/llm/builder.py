import os
from dotenv import load_dotenv

from langchain_google_genai import (ChatGoogleGenerativeAI,
                                    GoogleGenerativeAIEmbeddings)
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

class LargeLanguageModelBuilder:
    """
    Define a builder for various LLMs model to use in LangChain pipeline
    """
    load_dotenv()

    @staticmethod
    def get_open_ai_embedding(embedding_name: str = "text-embedding-3-small") -> OpenAIEmbeddings:
        try:
            api_key = os.environ["OPENAI_API_KEY"]
        except KeyError:
            raise ValueError("OPENAI_API_KEY is not set in the environment variables")
        return OpenAIEmbeddings(model=embedding_name, api_key=api_key)

    @staticmethod 
    def get_open_ai_llm(model_name: str = "gpt-4o-mini") -> ChatOpenAI:
        try:
            api_key = os.environ["OPENAI_API_KEY"]
        except KeyError:
            raise ValueError("OPENAI_API_KEY is not set in the environment variables")
        return ChatOpenAI(model=model_name, api_key=api_key)

    @staticmethod
    def get_google_gemini_embedding(embedding_name: str = "models/embedding-001") -> GoogleGenerativeAIEmbeddings:
        if not os.environ.get("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY is not set in the environment variables")
        return GoogleGenerativeAIEmbeddings(model=embedding_name)

    @staticmethod
    def get_google_gemini_llm(model_name: str = "gemini-1.5-flash") -> ChatGoogleGenerativeAI:
        if not os.environ.get("GOOGLE_API_KEY"):
            raise ValueError("GOOGLE_API_KEY is not set in the environment variables")
        return ChatGoogleGenerativeAI(model=model_name)

    @staticmethod
    def get_ollama_embedding(embedding_name: str = "llama3.2") -> OllamaEmbeddings:
        try:
            api_key = os.environ["OLLAMA_API_KEY"]
        except KeyError:
            raise ValueError("OLLAMA_API_KEY is not set in the environment variables")
        return OllamaEmbeddings(model=embedding_name, base_url=api_key)

    @staticmethod
    def get_ollama_llm(model_name: str = "llama3.2") -> OllamaLLM:
        try:
            api_key = os.environ["OLLAMA_API_KEY"]
        except KeyError:
            raise ValueError("OLLAMA_API_KEY is not set in the environment variables")
        return OllamaLLM(model=model_name, base_url=api_key)