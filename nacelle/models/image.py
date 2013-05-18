"""
Model used to store an image in the blobstore and provide
various convenience methods to serve it directly from there
"""
# stdlib imports
import base64
import hashlib
import imghdr
import logging

# third-party imports
import webapp2
from google.appengine.api import memcache
from google.appengine.ext import blobstore
from google.appengine.ext import ndb

# local imports
from nacelle.models.base import BaseModel
from nacelle.utils.blobstore import to_blobstore


class ImageModel(BaseModel):

    blob_key = ndb.BlobKeyProperty()
    image_type = ndb.StringProperty(choices=['image/gif', 'image/jpeg', 'image/png'], default='image/png')
    data_url_hash = ndb.StringProperty()

    def url(self, url_type):

        cache_key = 'image-url-' + str(self.blob_key) + '-' + url_type
        url = memcache.get(cache_key)
        if url is not None:
            return url

        if url_type == 'http':
            url = self.http_url
        elif url_type == 'data':
            url = self.data_url
        else:
            return None

        memcache.set(cache_key, url)
        return url

    @property
    def http_url(self):
        if self.blob_key is None:
            return None
        return webapp2.uri_for('blobstore-image', image_key=self.key.id())

    @property
    def data_url(self):
        try:
            data_url = self.file.encode("base64")
        except AttributeError:
            return None
        prefix = 'data:%s;base64,' % self.image_type
        data_url = prefix + data_url
        return data_url

    @property
    def file(self):

        if self.blob_key is None:
            return None

        cache_key = 'image-file-' + str(self.blob_key)
        image_file = memcache.get(cache_key)
        if image_file is not None:
            return image_file

        blob_reader = blobstore.BlobReader(self.blob_key)
        try:
            image_file = blob_reader.read()
        except IOError:
            return None

        try:
            memcache.set(cache_key, image_file)
        except ValueError:
            logging.warning('Image to big for cache, performance may suffer: %s' % str(self.blob_key))
        return image_file

    def update_from_data_url(self, data_url):

        """
        Accepts a data url, updating the image in blobstore if it's different
        """

        new_hash = hashlib.md5(data_url).hexdigest()
        if self.data_url_hash == new_hash:
            return self

        self.data_url_hash = new_hash
        self.image_type = data_url[5:].split(';', 1)[0]
        image_data = base64.b64decode(data_url[5:].split(';', 1)[1].split(',', 1)[1])
        self.blob_key = to_blobstore(image_data, mime_type=self.image_type)
        self.put()

    def update_from_binary_data(self, binary_blob):

        """
        Accepts a binary image, updating the image in blobstore if it's different
        """

        # autodetect image type
        image_type = 'image/' + imghdr.what('dummy', binary_blob)
        logging.info('Detected image type: %s' % image_type)

        # build data url from binary data
        data_url = 'data:%s;base64,' % image_type
        data_url += binary_blob.encode("base64")
        new_hash = hashlib.md5(data_url).hexdigest()
        if self.data_url_hash == new_hash:
            return self

        # save data url to blobstore and save model
        self.data_url_hash = new_hash
        self.image_type = image_type
        self.blob_key = to_blobstore(binary_blob, mime_type=image_type)
        self.put()
