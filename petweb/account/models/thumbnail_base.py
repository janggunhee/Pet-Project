import os
from django.conf import settings
from django.db import models
from versatileimagefield.fields import VersatileImageField, PPOIField
from versatileimagefield.placeholder import OnDiscPlaceholderImage


class ThumbnailBaseModel(models.Model):
    image = VersatileImageField(
        upload_to='upload_to',
        width_field='width',
        height_field='height',
    )
    ppoi = PPOIField()
    height = models.PositiveIntegerField(
        blank=True,
        null=True
    )
    width = models.PositiveIntegerField(
        blank=True,
        null=True
    )

    class Meta:
        abstract = True
