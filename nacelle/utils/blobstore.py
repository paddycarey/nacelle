# third-party imports
from google.appengine.api import files


def to_blobstore(data, mime_type='application/octet-stream'):

    """
    Function that accepts a (byte)string or binary data and writes it to the
    appengine blobstore, returning a BlobKey object.
    """

    # Create the file
    file_name = files.blobstore.create(mime_type=mime_type)

    # Open the file and write to it
    with files.open(file_name, 'a') as f:
        f.write(data)

    # Finalize the file. Do this before attempting to read it.
    files.finalize(file_name)

    # Get the file's blob key
    blob_key = files.blobstore.get_blob_key(file_name)

    return blob_key
