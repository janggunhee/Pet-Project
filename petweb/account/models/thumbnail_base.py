from django.db import models
from versatileimagefield.fields import VersatileImageField, PPOIField


class ThumbnailBaseModel(models.Model):
    class Meta:
        abstract = True
    image = VersatileImageField(
        'Image',
        upload_to='images/testimagemodel/',
        width_field='width',
        height_field='height'
    )
    ppoi = PPOIField()
    height = models.PositiveIntegerField(
        'Image Height',
        blank=True,
        null=True
    )
    width = models.PositiveIntegerField(
        'Image Width',
        blank=True,
        null=True
    )
