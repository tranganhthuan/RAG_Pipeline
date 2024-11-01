"""
Author: Trang Anh Thuan & Son Phat Tran
This file contains the logic for loading and saving text chunk for all documents within a folder
"""
import os
from typing import List

from module.text_segmentor import TextChunk, TextSegmentor
from module.vector_store import VectorStore


def is_valid_document(file_name: str) -> bool:
    """
    Check if the file is a valid document with a valid extension
    :param file_name: the name of the file
    :return: True if the file is a valid document, false otherwise
    """
    return file_name.endswith(".md")


def read_doc(file_path: str) -> str:
    """
    Read and return the content of a document file
    :param file_path: the path of the document
    :return: file content (str)
    """
    with open(file_path, "r", encoding="utf-8") as input_file:
        text = input_file.read()
    return text


def add_vectors_single_document(document_path: str,
                                text_segmentor: TextSegmentor,
                                vector_store: VectorStore) -> List[TextChunk]:
    """
    Add vectors from a new (single) document to vector store
    """
    # Read document and get vectors
    doc_content = read_doc(document_path)

    # Read to all text chunks
    text_chunks = text_segmentor.segment(os.path.basename(document_path), doc_content)

    # Save to vector store
    vector_store.add_multiple_documents([text_chunk.document for text_chunk in text_chunks])
    return text_chunks


def remove_vectors_single_document(document_path: str,
                                   vector_store: VectorStore):
    """
    Remove vectors from a document from a vector store
    """
    # Remove documents
    vector_store.delete_document(document_path)


def persist_vectors(document_folder: str,
                    text_segmentor: TextSegmentor,
                    vector_store: VectorStore) -> List[TextChunk]:
    """
    Read documents (markdown files) from a folder, convert it into text chunk,
    and save the chunks using vector store
    :param document_folder: directory of the documents
    :param text_segmentor
    :param vector_store
    :return:
    """
    # Read the files from document folder
    documents = os.listdir(document_folder)

    # Only keeps the valid documents
    filtered_documents = [doc for doc in documents if is_valid_document(doc)]

    # Save the chunks
    all_text_chunks = []

    # Convert to segment and save documents
    for doc_name in filtered_documents:
        # Read the document
        full_doc_path = os.path.join(document_folder, doc_name)
        doc_content = read_doc(full_doc_path)

        # Read to all text chunks
        text_chunks = text_segmentor.segment(doc_content)

        # Format the chunks
        for chunk in text_chunks:
            chunk.document_name = full_doc_path

        all_text_chunks.extend(text_chunks)

    # Finally save into vector store
    vector_store.save(all_text_chunks)
    return all_text_chunks

