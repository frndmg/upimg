import logging
import base64

from rest_framework import serializers

from . import models


log = logging.getLogger(__name__)


class ListImageSerializer(serializers.Serializer):
    images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False,
                                     use_url=False))

    def create(self, validated_data):
        images = validated_data.pop('images')

        data = []
        for img in images:
            img = models.Image(image=img, **validated_data)
            digest = img.get_digest()

            try:
                img = models.Image.objects.get(digest=digest)
            except models.Image.DoesNotExist:
                img.save()

            data.append(img.id)

        return data


class UploadTokenSerializer(serializers.ModelSerializer):
    expire_at = serializers.DateField()

    class Meta:
        model = models.UploadToken
        fields = ('id', 'expire_at', )
