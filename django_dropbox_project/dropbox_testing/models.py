from django.db import models
from django_dropbox.storage import DropboxStorage

STORAGE = DropboxStorage()


class Person(models.Model):
    photo = models.ImageField(upload_to='photos', storage=STORAGE, null=True, blank=True)
    resume = models.FileField(upload_to='resumes', storage=STORAGE, null=True, blank=True)
