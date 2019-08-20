from rest_framework import serializers

from . import models


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = ('id', 'image', 'meta', 'uploaded_at',)
        read_only_fields = ('image', 'meta',)
