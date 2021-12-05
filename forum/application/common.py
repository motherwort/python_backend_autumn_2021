from django.shortcuts import redirect
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import User


def require_authentication(view):
    def decorator(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return view(self, request, *args, **kwargs)
        else:
            return redirect('login')
    decorator.__name__ = view.__name__
    return decorator


class ModelSerializer(serializers.ModelSerializer):
    def is_valid(self, raise_exception=False):
        read_only_fields = getattr(self.Meta, 'read_only_fields', [])
        default_only_fields = getattr(self.Meta, 'default_only_fields', [])
        create_only_fields = getattr(self.Meta, 'create_only_fields', [])
        raise_exception_on_write_attempt = getattr(self.Meta, 'raise_exception_on_write_attempt', False)

        bad_data = {}
        for field in default_only_fields:
            if field in self.initial_data:
                bad_data[field] = self.initial_data.pop(field)
                if raise_exception_on_write_attempt:
                    if self.instance:
                        exc = ValidationError("Can't modify this field")
                    else:   
                        exc = ValidationError("This field sets automatically")
                    self._errors[field] = exc.detail

        super().is_valid(raise_exception=False)

        self.initial_data.update(bad_data)

        for field in self.initial_data:
            if (
                field in read_only_fields or
                field in create_only_fields and self.instance
            ):
                self._validated_data.pop(field, None)
                if raise_exception_on_write_attempt:
                    if field in read_only_fields:
                        exc = ValidationError("Can't write this field")
                    else:
                        exc = ValidationError("Can't modify this field")
                    self._errors[field] = exc.detail

        if self._errors and raise_exception:
            raise ValidationError(self.errors)

        return not bool(self._errors)


class ModelPKField(serializers.PrimaryKeyRelatedField):
    def __init__(self, model, fields=None, **kwargs):
        self._model = model
        assert type(fields) is list, "'fields' should be type of list or None"
        self._fields = fields
        if not 'queryset' in kwargs:
            self.queryset = model.objects.all()
        super().__init__(**kwargs)

    def to_representation(self, value):
        obj = self._model.objects.get(id=value.pk)
        if self._fields:
            if len(self._fields) == 1:
                return getattr(obj, self._fields[0])
            data = {
                field: getattr(obj, field)
                for field in self._fields
            }
            return data
        else:
            return str(obj)
