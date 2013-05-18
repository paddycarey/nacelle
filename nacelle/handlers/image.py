"""
Image related handlers
"""
# third-party imports
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

# local imports
from nacelle.models.image import ImageModel


class ImageHandler(blobstore_handlers.BlobstoreDownloadHandler):

    """
    This handler allows serving of images which have been stored
    using Nacelle's ImageModel. Responses will be cached for one
    hour on the client side.

    To use this handler insert the following route (or similar) in
    your app's routes module:

    RedirectRoute(
        r'/image/<image_key>',
        'nacelle.handlers.image.ImageHandler',
        strict_slash=True,
        name='blobstore-image'
    )

    """

    def get(self, image_key):

        # pull image model from datastore (or cache if present)
        image = ImageModel.get_by_id(image_key)
        if image is None:
            return self.error(404)

        # check that our blob key still exists in the datastore
        if not blobstore.get(image.blob_key):
            self.error(404)
        else:
            # set cache headers as appropriate
            self.response.headers['Cache-Control'] = 'public,max-age=3600'
            # send_blob adds custom headers to the response which appengine
            # intercepts and then replaces the response body with data from
            # the blobstore, serving the image directly from the blobstore
            self.send_blob(image.blob_key)
