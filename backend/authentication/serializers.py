from django.contrib.auth import get_user_model
from rest_framework import serializers

from users.models import UserTypes

User = get_user_model()


class UserSignUpSerializer(serializers.ModelSerializer):
    def create(self, validated_data) -> User:
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            company=validated_data['company'],
            image=validated_data['image'],
            user_type=(
                UserTypes.CUSTOMER if validated_data['user_type'].lower() == UserTypes.CUSTOMER
                else UserTypes.CONTRACTOR),
            is_active=True,
        )
        return user

    class Meta:
        model = User
        fields = ('username', 'email', 'company', 'image', 'password', 'user_type')


class TokenAnswerSerializer(serializers.Serializer):
    access = serializers.CharField()


class BadRequestSerializer(serializers.Serializer):
    message = serializers.CharField()
