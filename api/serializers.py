from rest_framework import serializers

from . import models


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = ('image', , 'meta', 'uploaded_at',)
        read_only_fields = ('meta', 'uploaded_at',)
