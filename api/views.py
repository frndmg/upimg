import logging

from django.shortcuts import get_object_or_404

from rest_framework import views
from rest_framework import parsers
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from PIL import Image
from PIL.ExifTags import TAGS

from . import models
from . import serializers

log = logging.getLogger(__name__)


def upload_link():
    """
    Generate a random token to be used as a new url to upload images
    """


class ImageUploadPermission(permissions.BasePermission):
    message = 'User does not request this upload link or expired'

    def has_permission(self, req, view):
        token = req.resolver_match.kwargs.get('token')
        try:
            up_token = models.UploadToken.objects.filter(token=token).get()
        except models.UploadToken.DoesNotExist:
            return False

        if req.user != up_token.user:
            return False

        return True


class ImageUploadView(views.APIView):
    parser_classes = (parsers.MultiPartParser, parsers.FileUploadParser,)
    permission_classes = (ImageUploadPermission,)

    def put(self, req, token, format=None):
        ids = {}

        # TODO: This could be batched and procesed in multiple process
        for k, v in req.data.items():
            ids[k] = models.Image.objects.create(image=v).id

        return Response(ids, status=status.HTTP_201_CREATED)


class ImageViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ImageSerializer
    queryset = models.Image.objects.all()
    


def statistics():
    pass
