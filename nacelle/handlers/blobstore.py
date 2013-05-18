"""
A collection of handlers that are useful for
serving data directly from the blobstore
"""
# stdlib imports
import logging
import urllib

# third-party imports
from google.appengine.api import images
from google.appengine.api import memcache
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

# local imports
from nacelle.handlers.base import BaseHandler


class BlobHandler(blobstore_handlers.BlobstoreDownloadHandler):

    """
    Serve a blob directly from the blobstore
    """

    def get(self, blob_key):

        # parse the blob key from the url and use it to get the
        # BlobInfo object we need
        blob_key = str(urllib.unquote(blob_key))
        blob_info = blobstore.BlobInfo.get(blob_key)
        logging.info(blob_info)

        # CORS Headers, 'cos that's how we roll
        self.response.headers['Access-Control-Allow-Origin'] = '*'
        self.response.headers['Cache-Control'] = 'public, max-age=31536000'

        # send the blob to the user. This is accomplished by setting some
        # custom headers on an empty response object. Appengine will detect
        # these headers and replace the response body with the correct data
        # from the blobstore.
        self.send_blob(blob_info)


class ImageHandler(BaseHandler):

    """
    Serve an image using the same high-speed image serving
    infrastructure Google uses to serve images from Picasa.

    URL Parameters:

    size=XX (optional)
        To resize an image, append size=XX to the end of the image URL, where XX
        is an integer from 0–1600 representing the new image size in pixels.
        The API resizes the image to the supplied value, applying the specified
        size to the image's longest dimension and preserving the original
        aspect ratio. For example, if you use size=32 to resize a 1200x1600 image,
        the resulting image is a 24x32. If that image were 1600x1200, the
        resized image would be 32x24 pixels.

    cropped=true (optional, default=false, only effective if size is required)
        To crop an image, append cropped=true to the end of the image URL,
        The API resizes the image to the supplied value, applying the
        specified size to the image's longest dimension and preserving the
        original aspect ratio. If the image is portrait, the API slices evenly
        from the top and bottom to make a square. If the image is landscape,
        the API slices evenly from the left and right to make a square. After
        cropping, the API resizes the image to the specified size.

    """

    def get(self, blob_key):

        # get image serving url from memcache
        image_url = memcache.get('image-' + blob_key)
        if image_url is None:
            # get serving url from images service
            image_url = images.get_serving_url(blob_key)
            # cache serving url for future retrieval
            memcache.set('image-' + blob_key, image_url)

        # transform image if requested
        if 'size' in self.request.GET:
            image_url += '=s%d' % int(self.request.get('size', default_value='NaN'))
            if not self.request.get('cropped', default_value='false') == 'false':
                image_url += '-c'

        # issue a permanent redirect (301) to the serving url
        return self.redirect(image_url, permanent=True)
