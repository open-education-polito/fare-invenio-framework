import os
import json


def read_menu_fields(key):
    choices = []
    filename = ""

    if key == "educationLevel":
        filename = "fare/file_management/education_level.json"
    if key == "subject":
        filename = "fare/file_management/subjects.json"

    with open(os.path.abspath(filename), "r") as json_file:
        data = json.loads(json_file.read())

    for element in data[key]:
        choices.append((element, element))

    choices.sort()
    return choices
