import logging

from django.shortcuts import render
from rest_framework import views
from rest_framework import parsers
from rest_framework.response import Response
from rest_framework import permissions

log = logging.getLogger(__name__)


def upload_link():
    """
    Generate a random token to be used as a new url to upload images
    """


class ImageUploadView(views.APIView):
    parser_classes = (parsers.MultiPartParser, parsers.FileUploadParser,)
    permission_classes = (permissions.AllowAny,)  # For now

    def put(self, req, token, format=None):
        # print(req)
        for k, v in req.data.items():
            # store file and return id
            log.debug(f'{k} {v}')

        return Response(status=204)


def get_image(id):
    pass


def statistics():
    pass
