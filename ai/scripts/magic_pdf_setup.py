"""
Author: MinerU authors
Modified and Clean by: Son Phat Tran
This file contains the code for the set-up of the Magic PDF library.
"""
import json
import os

import requests
from huggingface_hub import snapshot_download


def download_json(url):
    """
    Download json file from a specific URL
    :param url: the url of the JSON file
    :return: json content
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def download_and_modify_json(url, local_filename, modifications):
    """
    Download and modify the json template from MagicPDF to create a new local file
    :param url: the url of the template
    :param local_filename: local json file path to save to
    :param modifications: any modifications you want to make
    :return: None
    """
    if os.path.exists(local_filename):
        data = json.load(open(local_filename))
        config_version = data.get('config_version', '0.0.0')
        if config_version < '1.0.0':
            data = download_json(url)
    else:
        data = download_json(url)

    for key, value in modifications.items():
        data[key] = value

    with open(local_filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':

    miner_u_patterns = [
        "models/Layout/LayoutLMv3/*",
        "models/Layout/YOLO/*",
        "models/MFD/YOLO/*",
        "models/MFR/unimernet_small/*",
        "models/TabRec/TableMaster/*",
        "models/TabRec/StructEqTable/*",
    ]
    model_dir = snapshot_download('opendatalab/PDF-Extract-Kit-1.0', allow_patterns=miner_u_patterns)

    layout_reader_patterns = [
        "*.json",
        "*.safetensors",
    ]
    layout_reader_model_dir = snapshot_download('hantian/layoutreader', allow_patterns=layout_reader_patterns)

    model_dir = model_dir + '/models'
    print(f'model_dir is: {model_dir}')
    print(f'layout_reader_model_dir is: {layout_reader_model_dir}')

    json_url = 'https://github.com/opendatalab/MinerU/raw/master/magic-pdf.template.json'
    config_file_name = 'magic-pdf.json'
    home_dir = os.path.expanduser('~')
    config_file = os.path.join(home_dir, config_file_name)

    json_mods = {
        'models-dir': model_dir,
        'layout_reader-model-dir': layout_reader_model_dir,
    }

    download_and_modify_json(json_url, config_file, json_mods)
    print(f'The configuration file has been configured successfully, the path is: {config_file}')