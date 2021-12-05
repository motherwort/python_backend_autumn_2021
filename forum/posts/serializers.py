from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from application import common
from posts.models import Post
from threads.models import Thread
from users.models import User


class PostSerializer(common.ModelSerializer):
    thread = common.ModelPKField(Thread, ['id', 'title'])
    user = common.ModelPKField(
        User, ['id', 'username'], 
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Post
        fields = ['id', 'user', 'thread', 'content', 'created', 'is_edited']
        read_only_fields = ['id', 'created', 'is_edited']
        default_only_fields = ['user']
        create_only_fields = ['thread']

    # TODO сохранение оригинальной версии, проверка срока доступности изменения
    def update(self, instance, validated_data):
        full_data = validated_data.copy()
        # if instance.is_edited == False:
        #     full_data = validated_data.copy()
        #     full_data['unedited_content'] = instance.content
        instance.is_edited = True
        instance.save()
        return super().update(instance, full_data)
