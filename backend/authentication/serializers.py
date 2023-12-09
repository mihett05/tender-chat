from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import UserTypes

User = get_user_model()


class UserSignUpSerializer(serializers.ModelSerializer):
    def is_valid(self, *, raise_exception=False):
        types = UserTypes.CONTRACTOR.lower(), UserTypes.CUSTOMER.lower()
        if self.initial_data.get('user_type') not in types:
            raise ValidationError({"user_type": f"must be one of {types}"})

        if not self.initial_data.get('company'):
            raise ValidationError({"company": f"This field is required"})
        return super(UserSignUpSerializer, self).is_valid(raise_exception=raise_exception)

    def create(self, validated_data) -> User:
        print(validated_data)
        user = User.objects.create_user(
            email=self.initial_data['email'],
            username=self.initial_data['username'],
            password=self.initial_data['password'],
            company=self.initial_data['company'],
            image=self.initial_data.get('image', ''),
            user_type=(
                UserTypes.CUSTOMER if self.initial_data['user_type'].lower() == UserTypes.CUSTOMER
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
