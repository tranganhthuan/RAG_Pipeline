import os
import shutil

from module.markdown_converter import Converter
from module.markdown_converter.utils import convert_file
from module.pipeline import data_pipeline
from configs.config import (
    IMAGE_FOLDER,
    MARKDOWN_FOLDER,
    PDF_FOLDER,
    UPLOAD_FOLDER,
    CONVERTER,
)


class ConvertService:
    def __init__(self):
        self.data_pipeline = data_pipeline

    def get_file(self, file_name):
        source_path = os.path.join(UPLOAD_FOLDER, file_name)
        destination_path = os.path.join(PDF_FOLDER, file_name)
        shutil.move(source_path, destination_path)

    def convert_file_params_validation(
        self, input_path, output_path, image_output_path
    ):
        if not os.path.exists(input_path):
            raise ValueError(f"Input path {input_path} does not exist")
        if not os.path.exists(output_path):
            raise ValueError(f"Output path {output_path} does not exist")
        if not os.path.exists(image_output_path):
            raise ValueError(f"Image output path {image_output_path} does not exist")
        return True

    def convert_file(self, name):
        self.get_file(name)
        converter = Converter.get_converter(CONVERTER)
        convert_file(
            input_path=os.path.join(PDF_FOLDER, name),
            output_path=os.path.join(MARKDOWN_FOLDER),
            file_converter=converter(IMAGE_FOLDER),
        )

    def add_document(self, name):
        self.data_pipeline.add_single_document(os.path.join(MARKDOWN_FOLDER, name))

    def remove_document(self, name):
        self.data_pipeline.remove_single_document(name)
        if os.path.exists(os.path.join(MARKDOWN_FOLDER, name)):
            os.remove(os.path.join(MARKDOWN_FOLDER, name))
        if os.path.exists(os.path.join(IMAGE_FOLDER, name.replace(".md", ""))):
            shutil.rmtree(os.path.join(IMAGE_FOLDER, name.replace(".md", "")))
        if os.path.exists(os.path.join(PDF_FOLDER, name.replace(".md", ".pdf"))):
            os.remove(os.path.join(PDF_FOLDER, name.replace(".md", ".pdf")))

    def get_all_documents(self):
        return self.data_pipeline.get_all_documents()


convert_service = ConvertService()
