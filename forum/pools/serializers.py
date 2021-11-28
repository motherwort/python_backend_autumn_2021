from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from pools.models import Pool


class PoolSerializer(serializers.ModelSerializer):
    constant_fields = ['users', 'creator']
    creator = serializers.SerializerMethodField()
    users = serializers.SerializerMethodField()

    def get_creator(self, obj):
        return getattr(obj.creator, 'username', None)

    def get_users(self, obj):
        users = obj.users.all()
        users_str = [
            {
                'id': user.id,
                'username': str(user),
            }
            for user in users
        ]
        return users_str

    class Meta:
        model = Pool
        fields = ['id', 'name', 'description', 'users', 'creator', 'created']
        read_only_fields = ['created', 'users']
        
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
