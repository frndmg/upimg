import logging

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.crypto import get_random_string

from rest_framework import views
from rest_framework import parsers
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes, parser_classes

from PIL import Image
from PIL.ExifTags import TAGS

from . import models
from . import serializers
from . import permissions

log = logging.getLogger(__name__)


@api_view(['POST'])
def upload_link(req):
    """
    Generate a random token to be used as a new url to upload images
    """
    serializer = serializers.UploadTokenSerializer(data=req.data)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    token = get_random_string(16)
    serializer.save(token=token, user=req.user)

    return Response(reverse('upload', args=(token,)))


@api_view(['PUT'])
@parser_classes([parsers.MultiPartParser, parsers.FileUploadParser, ])
@permission_classes([permissions.ImageUploadPermission, ])
def upload_image(req, token):
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
