from rest_framework import serializers


# 출처(StackOverFlow): https://goo.gl/ZkVdwk
class MultiplePKsHyperlinkedIdentityField(serializers.HyperlinkedIdentityField):
    lookup_fields = ['pk']

    def __init__(self, view_name=None, **kwargs):
        self.lookup_fields = kwargs.pop('lookup_fields', self.lookup_fields)
        self.lookup_url_kwargs = kwargs.pop('lookup_url_kwargs', self.lookup_fields)

        assert len(self.lookup_fields) == len(self.lookup_url_kwargs)

        super(MultiplePKsHyperlinkedIdentityField, self).__init__(view_name, **kwargs)

    def get_object(self, view_name, view_args, view_kwargs):
        """
        Return the object corresponding to a matched URL.
        Takes the matched URL conf arguments, and should return an
        object instance, or raise an `ObjectDoesNotExist` exception.
        """
        lookup_kwargs = {
            key: view_kwargs[url_key]
            for key, url_key in zip(self.lookup_fields, self.lookup_url_kwargs)
        }
        return self.get_queryset().get(**lookup_kwargs)

    def get_url(self, obj, view_name, request, format):
        """
        Given an object, return the URL that hyperlinks to the object.
        May raise a `NoReverseMatch` if the `view_name` and `lookup_field`
        attributes are not configured to correctly match the URL conf.
        """
        # Unsaved objects will not yet have a valid URL.
        if hasattr(obj, 'pk') and obj.pk is None:
            return None

        kwargs = {
            url_key: getattr(obj, key)
            for key, url_key in zip(self.lookup_fields, self.lookup_url_kwargs)
        }

        return self.reverse(view_name, kwargs=kwargs, request=request, format=format)
