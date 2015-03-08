from six import BytesIO, advance_iterator
import os.path
import itertools

from dropbox.session import DropboxSession
from dropbox.client import DropboxClient
from dropbox.rest import ErrorResponse
from django.core.cache import cache
from django.core.files import File
from django.core.files.storage import Storage
from django.utils.encoding import filepath_to_uri

from .settings import (CONSUMER_KEY,
                       CONSUMER_SECRET,
                       ACCESS_TYPE,
                       ACCESS_TOKEN,
                       ACCESS_TOKEN_SECRET,
                       CACHE_TIMEOUT)


class DropboxStorage(Storage):
    """
    A storage class providing access to resources in a Dropbox Public folder.
    """

    def __init__(self, location='/Public'):
        session = DropboxSession(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TYPE, locale=None)
        session.set_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.client = DropboxClient(session)
        self.account_info = self.client.account_info()
        self.location = location
        self.base_url = 'http://dl.dropbox.com/u/{uid}/'.format(**self.account_info)

    def _get_abs_path(self, name):
        return os.path.realpath(os.path.join(self.location, name))

    def _open(self, name, mode='rb'):
        name = self._get_abs_path(name)
        remote_file = DropboxFile(name, self, mode=mode)
        return remote_file

    def _save(self, name, content):
        name = self._get_abs_path(name)
        directory = os.path.dirname(name)
        if not self.exists(directory) and directory:
            self.client.file_create_folder(directory)
        response = self.client.metadata(directory)
        if not response['is_dir']:
            raise IOError("%s exists and is not a directory." % directory)
        abs_name = os.path.realpath(os.path.join(self.location, name))
        self.client.put_file(abs_name, content)
        return name

    def delete(self, name):
        name = self._get_abs_path(name)
        self.client.file_delete(name)

    def exists(self, name):
        name = self._get_abs_path(name)
        try:
            metadata = self.client.metadata(name)
            if metadata.get('is_deleted'):
                return False
        except ErrorResponse as e:
            if e.status == 404:  # not found
                return False
            raise e
        return True

    def listdir(self, path):
        path = self._get_abs_path(path)
        response = self.client.metadata(path)
        directories = []
        files = []
        for entry in response.get('contents', []):
            if entry['is_dir']:
                directories.append(os.path.basename(entry['path']))
            else:
                files.append(os.path.basename(entry['path']))
        return directories, files

    def size(self, name):
        cache_key = 'django-dropbox-size:%s' % filepath_to_uri(name)
        size = cache.get(cache_key)

        if not size:
            size = self.client.metadata(filepath_to_uri(name))['bytes']
            cache.set(cache_key, size, CACHE_TIMEOUT)

        return size

    def url(self, name):
        cache_key = 'django-dropbox-url:%s' % filepath_to_uri(name)
        url = cache.get(cache_key)

        if not url:
            url = self.client.share(filepath_to_uri(name), short_url=False)['url'].replace('?dl=0', '?dl=1')
            cache.set(cache_key, url, CACHE_TIMEOUT)

        return url

    def get_available_name(self, name):
        """
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.
        """
        name = self._get_abs_path(name)
        dir_name, file_name = os.path.split(name)
        file_root, file_ext = os.path.splitext(file_name)
        # If the filename already exists, add an underscore and a number (before
        # the file extension, if one exists) to the filename until the generated
        # filename doesn't exist.
        count = itertools.count(1)
        while self.exists(name):
            # file_ext includes the dot.
            name = os.path.join(dir_name, "%s_%s%s" % (file_root, advance_iterator(count), file_ext))

        return name


class DropboxFile(File):
    def __init__(self, name, storage, mode):
        self._storage = storage
        self._mode = mode
        self._is_dirty = False
        self.file = BytesIO()
        self.start_range = 0
        self._name = name

    @property
    def size(self):
        if not hasattr(self, '_size'):
            self._size = self._storage.size(self._name)
        return self._size

    def read(self, num_bytes=None):
        return self._storage.client.get_file(self._name).read()

    def write(self, content):
        if 'w' not in self._mode:
            raise AttributeError("File was opened for read-only access.")
        self.file = BytesIO(content)
        self._is_dirty = True

    def close(self):
        if self._is_dirty:
            self._storage.client.put_file(self._name, self.file.getvalue())
        self.file.close()
