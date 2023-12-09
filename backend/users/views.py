from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import (mixins, status)
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from authentication.serializers import BadRequestSerializer
from users.serializers import UserProfileSerializer, UserPasswordChangeSerializer, UserProfileEditSerializer

User = get_user_model()


class UserView(mixins.RetrieveModelMixin,
               mixins.ListModelMixin,
               GenericViewSet):
    """
    View for get retrieve/list of users
    """

    queryset = User.objects.all()
    serializer_class = UserProfileSerializer


class UserPrivateDataView(mixins.UpdateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.RetrieveModelMixin,
                          GenericViewSet):
    """
    View for change/get active user profile data
    """

    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    action_serializers = {
        'retrieve': UserProfileSerializer,
        'update': UserProfileEditSerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(UserPrivateDataView, self).get_serializer_class()

    def get_object(self):
        return self.request.user

    @extend_schema(responses={400: BadRequestSerializer, 200: UserProfileSerializer})
    def retrieve(self, request: Request, pk=None, *args, **kwargs) -> Response:
        """handler for getting profile data of an active user"""
        return Response({'message': self.get_serializer(instance=request.user).data}, status=status.HTTP_200_OK)

    @extend_schema(request=UserProfileEditSerializer, responses={400: BadRequestSerializer, 200: UserProfileSerializer})
    def update(self, request: Request, *args, **kwargs) -> Response:
        """handler for update user profile data"""

        serialized: UserProfileEditSerializer = self.get_serializer(data=request.data)
        serialized.is_valid(raise_exception=True)

        serialized.update(request.user, serialized.initial_data)
        return Response(UserProfileSerializer(instance=request.user).data, status=status.HTTP_200_OK)

    @extend_schema(request=UserPasswordChangeSerializer, responses={400: BadRequestSerializer, 200: str})
    def partial_update(self, request: Request, *args, **kwargs) -> Response:
        """handler for update user password"""

        serialized = UserPasswordChangeSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)

        serialized.update(request.user, serialized.initial_data)
        return Response({'message': 'Password changed'}, status=status.HTTP_200_OK)

    @extend_schema(responses={204: BadRequestSerializer, 200: BadRequestSerializer})
    def destroy(self, request: Request, *args, **kwargs) -> Response:
        """handler for delete user"""

        user = request.user
        user.is_active = False
        user.save()

        return Response({'message': 'User was successfully deleted'}, status=status.HTTP_200_OK)
