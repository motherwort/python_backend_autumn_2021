from rest_framework import serializers
from application import common
from pools.models import Pool
from users.models import User


class UserListingField(serializers.RelatedField):
    def to_representation(self, user):
        user_repr = {
            'id': user.id,
            'username': str(user),
        }
        return user_repr


class PoolSerializer(common.ModelSerializer):
    users = UserListingField(read_only=True, many=True)
    creator = common.ModelPKField(
        User, ['id', 'username'], 
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Pool
        fields = ['id', 'name', 'description', 'users', 'creator', 'created']
        read_only_fields = ['id', 'users', 'created']
        default_only_fields = ['creator']