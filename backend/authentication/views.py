from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import (mixins, status)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.serializers import TokenRefreshSerializer, TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from authentication.serializers import (
    BadRequestSerializer,
    TokenAnswerSerializer, UserSignUpSerializer,

)
from authentication.utils import make_response

User = get_user_model()


class UserLoginView(TokenObtainPairView):
    @extend_schema(request=TokenObtainPairSerializer, responses={400: BadRequestSerializer, 200: TokenAnswerSerializer})
    def post(self, request: Request, *args, **kwargs) -> Response:
        return make_response(super(UserLoginView, self).post(request, *args, **kwargs))


class UserLoginRefreshView(TokenRefreshView):
    @extend_schema(request=TokenRefreshSerializer, responses={400: BadRequestSerializer, 200: TokenAnswerSerializer})
    def post(self, request: Request, *args, **kwargs) -> Response:
        return make_response(super(UserLoginRefreshView, self).post(request, *args, **kwargs))


class UserRegistrationView(mixins.CreateModelMixin, GenericViewSet):
    """
    View for registrate new users
    """

    serializer_class = UserSignUpSerializer

    @extend_schema(request=UserSignUpSerializer, responses={400: BadRequestSerializer, 200: TokenAnswerSerializer})
    def create(self, request: Request) -> Response:
        """handler for create user"""

        serializer: UserSignUpSerializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        refresh = RefreshToken.for_user(serializer.instance)
        response = Response(
            {'access': str(refresh.access_token)},
            status=status.HTTP_201_CREATED, headers=self.get_success_headers(serializer.data)
        )
        response.set_cookie(key='refresh', value=str(refresh))

        return response
