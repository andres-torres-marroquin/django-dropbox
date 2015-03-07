# django-dropbox
> Version 0.0.1

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

set DEFAULT_FILE_STORAGE in settings.py :

    DEFAULT_FILE_STORAGE = 'django_dropbox.storage.DropboxStorage'

additionally you must need to set the next settings:

    DROPBOX_CONSUMER_KEY = 'xxx'
    DROPBOX_CONSUMER_SECRET = 'xxx'
    DROPBOX_ACCESS_TOKEN = 'xxx'
    DROPBOX_ACCESS_TOKEN_SECRET = 'xxx'

if you don't have `DROPBOX_CONSUMER_KEY` or `DROPBOX_CONSUMER_SECRET` 
you will need to create an Dropbox app at [Dropbox for Developers](https://www.dropbox.com/developers)
then set `DROPBOX_CONSUMER_KEY` and `DROPBOX_CONSUMER_SECRET` settings in `settings.py`,
after that run:

    $ python manage.py get_dropbox_token

And follow up on screen instructions, finally set the `DROPBOX_ACCESS_TOKEN` and `DROPBOX_ACCESS_TOKEN_SECRET` in `settings.py`

