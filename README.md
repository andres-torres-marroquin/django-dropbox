# django-dropbox
> Version 0.1.2

# What

django-dropbox is a Django App that contains a Django Storage which uses Dropbox.

# Installing

## First of all

    pip install django-dropbox

## Add it to your Django Project

INSTALLED_APPS on settings.py

    INSTALLED_APPS = (
        ...
        'django_dropbox',
        ...
    )

additionally you must need to set the next settings:

    DROPBOX_ACCESS_TOKEN = 'xxx'

if you don't have `DROPBOX_ACCESS_TOKEN` you can create one after creating a Dropbox app at [Dropbox for Developers](https://www.dropbox.com/developers).
If you have your Dropbox `App key` and `App secret`, you can set `DROPBOX_CONSUMER_KEY` and `DROPBOX_CONSUMER_SECRET` settings in `settings.py`, then run:

    $ python manage.py get_dropbox_token

And follow up on screen instructions, finally set the  and `DROPBOX_ACCESS_TOKEN_SECRET` in `settings.py`


# Contributing
When contributing, please follow these steps:

* Clone the repo and make your changes.
* Make sure your code has test cases written against it.
* Make sure all the tests pass.
* Lint your code with Flake8.
* Add your name to the list of contributers.
* Submit a Pull Request.

## Tests

Tests are written following Django best practices. You can run them all easily using the example django_project.

```
$ cd django_dropbox_project
$ python manage.py test --settings=settings
```

To check the unit tests coverage you can:
```
$ pip install coverage
$ cd django_dropbox_project
$ coverage run manage.py test --settings=settings
$ coverage report -m
```
