# FARE
> The Free Architecture for Remote Education

![https://travis-ci.org/open-education-polito-it/fare-platform](https://img.shields.io/travis/open-education-polito/fare-platform.svg)

![https://coveralls.io/r/open-education-polito/fare-platform](https://img.shields.io/coveralls/open-education-polito/fare-platform.svg)

![https://github.com/open-education-polito/fare-platform/blob/master/LICENSE](https://img.shields.io/github/license/open-education-polito/fare-platform.svg)

Free Architecture for Remote Education

Further documentation will be available on
> https://fare.readthedocs.io/ #TODO

- [Steps to create the module](#step-to-create-the-module)

# Steps to create the module

In order to define the feature's module the following steps were performed:
* added the creation of `staff role` in `fare-platform/script/setup` 
* creation of the `grant_staff` folder in `fare-platform/fare`
* creation of the StaffForm form in `grant_staff/forms.py`
* creation of the grant view in `fare-platform/fare/grant_staff/views.py` with the appropriate check, through decorators, of the right permission to access to it
* creation of the templates path `templates/grant_staff`
* creation of the templates for success or failure
* creationof the API in `fare-platform/fare/grant_staff/api.py`
* added the module inside the `invenio_base.blueprints` in the file `fare-platform/setup.py`
* reinstall the app to add the module with `pipenv run pip install -e .`

