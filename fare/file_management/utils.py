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


def arguments():
    """
    Used for the view to retrieve
    the arguments of each subject
    """
    return ARGUMENTS


def init_field():
    """
    Initialize the field of the coverage with
    the arguments of the default subject, that
    is the first element of the sorted array
    """
    data = SUBJECTS
    subjects = []
    arguments_list = []

    for subject in data["subject"]:
        subjects.append(subject)

    subjects.sort()

    if ARGUMENTS.get(subjects[0]) is None:
        return [("", "")]

    for argument in ARGUMENTS[subjects[0]]:
        arguments_list.append((argument, argument))

    return arguments_list
