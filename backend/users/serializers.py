from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserProfileEditSerializer(serializers.ModelSerializer):
    def is_valid(self, *, raise_exception=False):
        if not any(self.initial_data.values()):
            raise ValidationError("You should pass at least one field")
        if not all(self.initial_data.values()):
            raise ValidationError("You should pass non-empty value for all fields you wanna change")
        return super(UserProfileEditSerializer, self).is_valid(raise_exception=raise_exception)

    class Meta:
        model = User
        fields = ('username', 'email', 'image')
        extra_kwargs = {
            'email': {'required': False},
            'image': {'required': False},
            'username': {'required': False},
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'image', 'company', 'user_type')


class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def update(self, instance: User, validated_data):
        if not instance or not instance.check_password(validated_data['old_password']):
            raise ValidationError('old_password is incorrect')

        instance.set_password(validated_data['new_password'])
        instance.save()

    class Meta:
        model = User
        fields = ('username', 'old_password', 'new_password')
