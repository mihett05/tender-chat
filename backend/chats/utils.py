import difflib
import json
import os
import string
from random import choices
from typing import List

from docxtpl import DocxTemplate

from __config__.config import BACKEND_PATH
from chats.conv import num2text


def simple_json_comparison(old_version: dict, new_version: dict) -> List[str]:
    old = json.dumps(old_version, indent=4).splitlines()
    new = json.dumps(new_version, indent=4).splitlines()

    return list(difflib.Differ().compare(old, new))


def example_comp():
    text1 = {"field_1": "field_1", "field_2": "field_2"}
    text2 = {"field_1": "update", "field_2": "field_2"}

    obj = simple_json_comparison(text1, text2)

    print(obj)
    print(*obj, sep='\n')


def create_word(data: dict, file_path=''.join(choices(string.ascii_letters + '0123456789', k=16))):
    # open template
    path = BACKEND_PATH
    doc = DocxTemplate(f"{path}/static/tpl.docx")

    for key, value in data.items():
        value: str
        if value.isdigit():
            data[f'{key}_string'] = num2text(int(value))

    # render & save docx file
    doc.render(data)
    doc.save(f"{path}/media/{file_path}.docx")
    return f"/media/{file_path}.docx"
