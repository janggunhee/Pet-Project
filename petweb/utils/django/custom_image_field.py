from django.conf import settings
from django.db.models.fields.files import ImageField, ImageFieldFile
from django.utils.module_loading import import_string


class CustomImageFieldFile(ImageFieldFile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if (not self.name or self.name == self.field.static_image_path) and self.field.static_image_path:
            self.name = self.field.static_image_path
            self.storage = import_string(settings.STATICFILES_STORAGE)()


class CustomImageField(ImageField):
    attr_class = CustomImageFieldFile

    def __init__(self, *args, **kwargs):
        self.static_image_path = kwargs.pop('default_static_image', 'placeholder/placeholder_human.png')
        super().__init__(*args, **kwargs)
