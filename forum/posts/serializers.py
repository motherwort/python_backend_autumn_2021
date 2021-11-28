from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    constant_fields = ['user', 'thread']

    user = serializers.SerializerMethodField()
    thread = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username
        # user = obj.user
        # user_data = {
        #         'id': user.id,
        #         'username': user.username,
        #     }
    
    def get_thread(self, obj):
        return obj.thread.title

    class Meta:
        model = Post
        fields = ['id', 'user', 'thread', 'content', 'created', 'is_edited']
        read_only_fields = ['created', 'is_edited']

    # TODO сохранение оригинальной версии, проверка срока доступности изменения
    def update(self, instance, validated_data):
        print(validated_data)
        full_data = validated_data.copy()
        # if instance.is_edited == False:
        #     full_data = validated_data.copy()
        #     full_data['unedited_content'] = instance.content
        instance.is_edited = True
        return super().update(instance, full_data)
        
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
