import logging

from rest_framework import views
from rest_framework import parsers
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from PIL import Image
from PIL.ExifTags import TAGS

from . import models

log = logging.getLogger(__name__)


def upload_link():
    """
    Generate a random token to be used as a new url to upload images
    """


class ImageUploadView(views.APIView):
    parser_classes = (parsers.MultiPartParser, parsers.FileUploadParser,)
    permission_classes = (permissions.AllowAny,)  # For now

    def put(self, req, token, format=None):
        ids = {}

        # TODO: This could be batched and procesed in multiple process
        for k, v in req.data.items():
            ids[k] = models.Image.objects.create(image=v).id

        return Response(ids, status=status.HTTP_201_CREATED)


def get_image(id):
    pass


def statistics():
    pass
