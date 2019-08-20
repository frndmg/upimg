import imghdr
import hashlib
import logging

from django.conf import settings
from django.dispatch import receiver
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.postgres.fields import HStoreField, JSONField
from django.utils import timezone

from rest_framework.authtoken.models import Token

import PIL
from PIL.ExifTags import TAGS

log = logging.getLogger(__name__)


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    meta = HStoreField()

    digest = models.CharField(max_length=64, blank=True, editable=False)

    uploaded_at = models.DateTimeField(auto_now=True)

    def exif_meta(self):
        meta = {}
        self.image.seek(0)
        img = PIL.Image.open(self.image)

        try:
            info = img._getexif()
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                meta[decoded] = value
        except AttributeError:
            pass
        meta['format'] = img.format
        return meta

    def compute_digest(self):
        h = hashlib.sha1()
        self.image.seek(0)

        if self.image.multiple_chunks():
            for chunk in self.image.chunks():
                h.update(chunk)
        else:
            h.update(self.image.read())

        return h.hexdigest()

    def save(self, *args, **kwargs):
        digest = self.compute_digest()

        image = Image.objects.filter(digest=digest).first()
        if image is not None:
            image = image.image
            log.debug('using existant image: {}'.format(self.image))
            self.image = image

        self.digest = digest
        self.meta = self.exif_meta()

        super(Image, self).save(*args, **kwargs)

    def __str__(self):
        return self.image.url


class UploadToken(models.Model):
    token = models.CharField(max_length=256)

    expire_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now=True)

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='tokens')

    @property
    def expired(self):
        return self.expire_at <= timezone.now()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
