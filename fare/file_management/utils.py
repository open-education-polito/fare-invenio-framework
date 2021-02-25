from ..records.config import FARE_EDUCATION_LEVEL, FARE_SUBJECTS, FARE_ARGUMENTS


def read_menu_fields(key):
    """
    Use the key passed to retrieve
    the corresponding json element
    and set the values in the field
    """
    choices = []
    data = ""

    if key == "educationLevel":
        data = FARE_EDUCATION_LEVEL
    if key == "subject":
        data = FARE_SUBJECTS

    for element in data[key]:
        choices.append((element, element))

    choices.sort()
    return choices


def get_all_arguments():
    """
    Used to retrieve
    the arguments of each subject
    """
    return FARE_ARGUMENTS


def get_all_subjects():
    """
    Used to retrieve
    all subjects
    """
    return FARE_SUBJECTS


def get_all_education_levels():
    """
    Used to retrieve
    all education levels
    """
    return FARE_EDUCATION_LEVEL


def init_field_all():
    """
    Initialize the field coverage with
    all the arguments
    """
    arguments_list = []

    for subject in FARE_ARGUMENTS.keys():
        for argument in FARE_ARGUMENTS[subject]:
            arguments_list.append((argument, argument))

    return arguments_list
