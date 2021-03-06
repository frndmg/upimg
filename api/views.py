import logging
import base64
import imghdr
from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponse, HttpResponseServerError
from django.utils.crypto import get_random_string
from django.db.models import Count
from django.utils import timezone

from rest_framework import views
from rest_framework import parsers
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
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
    """
    Upload the image given the token
    """
    serializer = serializers.ListImageSerializer(data=req.data)
    if not serializer.is_valid():
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    ids = serializer.save()
    return Response(ids, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_image(req, pk):
    image = get_object_or_404(models.Image, pk=pk)

    with image.image.open() as fp:
        data = fp.read()
        fmt = image.meta.get('format', imghdr.what(fp))
        return HttpResponse(data, content_type='image/{}'.format(fmt))

    return HttpResponseServerError('problem reading image')


@api_view(['GET'])
def statistics(req):
    common_models = models.Image.objects\
        .filter(meta__has_key='Model')\
        .values('meta__Model')\
        .annotate(count=Count('meta__Model'))

    common_formats = models.Image.objects\
        .filter(meta__has_key='format')\
        .values('meta__format')\
        .annotate(count=Count('meta__format'))

    days = 30
    upload_freq_per_day = models.Image.objects\
        .filter(uploaded_at__gte=timezone.now() - timedelta(days=days)).count() / days 

    return Response({
        'common_models': common_models,
        'common_formats': common_formats,
        'uploaded_freq_per_day': upload_freq_per_day,
    }, status=status.HTTP_200_OK)
