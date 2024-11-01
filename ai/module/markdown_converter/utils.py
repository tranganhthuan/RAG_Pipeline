"""
Author: Trang Anh Thuan & Son Phat Tran
This file contains the logic of converting PDFs file in a folder to Markdown files
"""

import os
from module.markdown_converter.converter import MarkdownConverter


def convert_file(input_path: str, output_path: str, file_converter: MarkdownConverter):
    """
    Convert a single PDF file to markdown and save it in output path
    :param input_path: input directory that contains PDF files
    :param output_path: output directory for the markdown files
    :param file_converter: markdown converter
    :return: None
    """
    # Get the name of the file without extension (.pdf)
    pdf_file_name = os.path.basename(input_path)
    file_name_without_extension = pdf_file_name.split(".")[0]

    # Get the PDF content
    file_content = file_converter.convert(input_path)

    # Save to output file
    markdown_file_path = os.path.join(output_path, f"{file_name_without_extension}.md")
    with open(markdown_file_path, "w", encoding="utf-8") as output_file:
        output_file.write(file_content)


def convert_folder(
    input_path: str, output_path: str, file_converter: MarkdownConverter
):
    """
    Convert all PDFs file in the folder to markdown and save them in output path
    :param input_path: input directory that contains PDF files
    :param output_path: output directory for the markdown files
    :param file_converter: markdown converter
    :return: None
    """
    # Get all the files from input path
    pdf_file_names = [file for file in os.listdir(input_path) if file.endswith(".pdf")]

    # Convert all pdf files
    for pdf_file_name in pdf_file_names:
        file_path = os.path.join(input_path, pdf_file_name)
        convert_file(file_path, output_path, file_converter)
