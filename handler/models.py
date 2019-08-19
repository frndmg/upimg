from django.contrib.postgres.fields import HStoreField
from django.contrib.gis.db import gis_models

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    meta = HStoreField()

    uploaded_at = models.DateTimeField(auto_now=True)
