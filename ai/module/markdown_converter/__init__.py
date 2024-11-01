"""
Author: Trang Anh Thuan & Son Phat Tran
This file contains the example usage of converting PDFs file in a folder to Markdown files
"""
from module.markdown_converter.converter import MinerUConverter, LlamaParseConverter

class Converter:
    @staticmethod
    def get_converter(converter_name: str):
        dict_converter = {
            "llama_parse": LlamaParseConverter,
            "miner_u": MinerUConverter,
        }
        converter = dict_converter.get(converter_name, None)
        if converter is None:
            raise ValueError(f"Converter {converter_name} not found")
        return converter

