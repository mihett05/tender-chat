import difflib
import json
from pprint import pprint
from typing import List


def simple_json_comparison(old_version: dict, new_version: dict) -> List[str]:
    old = json.dumps(old_version, indent=4).splitlines()
    new = json.dumps(new_version, indent=4).splitlines()

    return list(difflib.Differ().compare(old, new))


def example():
    text1 = {"field_1": "field_1", "field_2": "field_2"}
    text2 = {"field_1": "update", "field_2": "field_2"}

    obj = simple_json_comparison(text1, text2)

    print(obj)
    print(*obj, sep='\n')
