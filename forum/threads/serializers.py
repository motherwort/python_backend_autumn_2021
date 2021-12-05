from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from application import common
from pools.models import Pool
from threads.models import Thread
from users.models import User


class ThreadSerializer(common.ModelSerializer):
    pool = common.ModelPKField(Pool, ['id', 'name'])
    creator = common.ModelPKField(
        User, ['id', 'username'], 
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Thread
        fields = ['id', 'pool', 'title', 'description', 'creator']
        read_only_fields = ['id']
        default_only_fields = ['creator']
        create_only_fields = ['pool']

    # TODO сохранение оригинальной версии/
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
