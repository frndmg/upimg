from rest_framework import serializers
from rest_framework import fields

from . import models


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = ('id', 'image', 'meta', 'uploaded_at',)
        read_only_fields = ('image', 'meta',)


class UploadTokenSerializer(serializers.ModelSerializer):

    expire_at = fields.DateField()

    class Meta:
        model = models.UploadToken
        fields = ('id', 'expire_at', )
