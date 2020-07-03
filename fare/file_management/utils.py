from ..records.config import EDUCATION_LEVEL, SUBJECTS, ARGUMENTS


def read_menu_fields(key):
    """
    Use the key passed to retrieve
    the corresponding json element
    and set the values in the field
    """
    choices = []
    data = ""

    if key == "educationLevel":
        data = EDUCATION_LEVEL
    if key == "subject":
        data = SUBJECTS

    for element in data[key]:
        choices.append((element, element))

    choices.sort()
    return choices


def get_all_arguments():
    """
    Used to retrieve
    the arguments of each subject
    """
    return ARGUMENTS


def init_field_all():
    """
    Initialize the field coverage with
    all the arguments
    """
    arguments_list = []

    for subject in ARGUMENTS.keys():
        for argument in ARGUMENTS[subject]:
            arguments_list.append((argument, argument))

    return arguments_list
