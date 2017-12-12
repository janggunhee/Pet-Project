import os
from django.conf import settings
from django.db import models
from versatileimagefield.fields import VersatileImageField, PPOIField
from versatileimagefield.placeholder import OnDiscPlaceholderImage


class ThumbnailBaseModel(models.Model):
    image = VersatileImageField(
        upload_to='thumbnails/',
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
    optional_image = VersatileImageField(
        upload_to='pet/optional/',
        blank=True,
        placeholder_image=OnDiscPlaceholderImage(
            path=os.path.join(
                settings.ROOT_DIR,
                '.media',
                'placeholder.gif'
            )
        )
    )
    class Meta:
        abstract = True
