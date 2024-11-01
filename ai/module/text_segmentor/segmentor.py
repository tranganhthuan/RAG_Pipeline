from abc import ABC, abstractmethod
from typing import List

from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document

class TextChunk:
    def __init__(self, content: str, document_name: str = "", chunk_location: int = -1):
        """
        Contains the information of a text chunk
        :param content: the content of the text chunk (str)
        :param document_name: the name of the document of the text (str)
        :param chunk_location: the location of the chunk (str)
        """
        self.content = content
        self.document_name = document_name
        self.chunk_location = chunk_location
        self.document = Document(page_content=content, metadata={"source": document_name, "location": chunk_location})

    def __str__(self):
        """
        Get the string representation of the chunk
        :return: representation of the chunk as a string
        """
        return f"text: {self.content} - document_name: {self.document_name} - chunk_location: {self.chunk_location}"


class TextSegmentor(ABC):
    @abstractmethod
    def segment(self, name: str, content: str) -> List[TextChunk]:
        pass


class MarkDownHeaderSegmentor(TextSegmentor, ABC):
    def __init__(self):
        """
        Create LangChain Markdown Segmentor based on the header
        """
        headers = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        self.splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers)

    def segment(self, name: str, content: str) -> List[TextChunk]:
        """
        Split the text from document into chunks
        :param text: the text of the document
        :return: list of text chunk
        """
        # Split the text into chunks
        chunks = self.splitter.split_text(content)

        # Create the result
        return [
            TextChunk(content=chunk.page_content,
                      document_name=name,
                      chunk_location=index)
            for index, chunk in enumerate(chunks)
        ]