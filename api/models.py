from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import HStoreField


class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    meta = HStoreField(max_length=256)

    uploaded_at = models.DateTimeField(auto_now=True)


class UploadToken(models.Model):
    token = models.CharField(max_length=256)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tokens')
