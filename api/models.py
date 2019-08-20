from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import HStoreField, JSONField
from django.utils import timezone

import PIL
from PIL.ExifTags import TAGS


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    meta = HStoreField()

    uploaded_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        img = PIL.Image.open(self.image)

        meta = {}

        try:
            info = img._getexif()

            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                meta[decoded] = value
        except AttributeError:
            pass

        self.meta = meta

        super(Image, self).save(*args, **kwargs)


class UploadToken(models.Model):
    token = models.CharField(max_length=256)
    
    expire_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')

    @property
    def expired(self):
        return self.expire_at <= timezone.now()
