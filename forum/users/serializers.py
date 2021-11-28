from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'name', 'email', 'user_info', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def save(self, **kwargs):
        try:
            super().save(**kwargs)
        except Exception as exc:
            raise exc
        else:
            # Updating password if new_password in validated_data
            if (self.instance is not None) and ('new_password' in self.validated_data):
                self.instance.password = self.validated_data['new_password']
                self.instance.save()

        return self.instance

    def is_valid(self, raise_exception=False):
        super().is_valid(raise_exception=False)

        #Checking if password is in data
        if 'password' not in self.initial_data:
            exc = ValidationError("Password required")
            self._errors['password'] = exc.detail

        # Checking password if update
        if (self.instance is not None) and ('password' in self.validated_data):
            pwd = self.validated_data['password']
            if pwd != self.instance.password:
                self.validated_data.pop('password')
                exc = ValidationError("Wrong password")
                self._errors['password'] = exc.detail

        # Validating new_password
        if 'new_password' in self.initial_data:
            try:
                new_pwd = self.validate_password(self.initial_data['new_password'])
            except ValidationError as exc:
                self._errors['new_password'] = exc.detail
            else:
                self._validated_data['new_password'] = new_pwd

        if self._errors and raise_exception:
            raise ValidationError(self.errors)

        return not bool(self._errors)
    
    # TODO формат пароля установить
    def validate_password(self, value):
        if value is None:
            raise serializers.ValidationError("Password required")
        if not isinstance(value, str):
            raise serializers.ValidationError("Password has to be type of string")
        if len(value) < 4:
            raise serializers.ValidationError("Password too short. Requires 4 characters minimum")
        return value