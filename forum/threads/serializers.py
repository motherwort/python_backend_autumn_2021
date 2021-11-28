from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from threads.models import Thread


class ThreadSerializer(serializers.ModelSerializer):
    constant_fields = ['pool', 'creator']

    pool = serializers.SerializerMethodField()
    creator = serializers.SerializerMethodField()

    def get_pool(self, obj):
        return obj.pool.name

    def get_creator(self, obj):
        return getattr(obj.creator, 'username', None)

    class Meta:
        model = Thread
        fields = ['id', 'pool', 'title', 'description', 'creator']

    # TODO сохранение оригинальной версии/
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception=False)

        # Don't allow modification of fields in self.constant_fields
        if self.instance is not None:
            for field in self.constant_fields:
                if field in self.initial_data:
                    exc = ValidationError("Can't modify this field")
                    self._errors[field] = exc.detail

        if self._errors and raise_exception:
            raise ValidationError(self.errors)

        return not bool(self._errors)
