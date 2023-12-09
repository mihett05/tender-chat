from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Q
from drf_spectacular.utils import extend_schema
from rest_framework import (mixins, status, serializers)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from authentication.serializers import BadRequestSerializer
from chats.models import Contract, Commit, Message
from chats.schemes import ContractCreateRequest, ContractCreateResponse, ContractDetailResponse, ContractListResponse, \
    CommitCreateRequest, CommitUpdateRequest, MessageCreateRequest, MessageCreateResponse, CommitCreateResponse
from chats.serializers import (
    ContractCreateSerializer, ContractListSerializer, ContractDetailSerializer,
    CommitCreateSerializer, CommitDetailSerializer, CommitListSerializer,
    MessageDetailSerializer, MessageListSerializer,
)
from users.permissions import IsChatParticipant, IsCustomer

User = get_user_model()


class ContractCreateView(mixins.CreateModelMixin, GenericViewSet):
    """
    View for get/set/delete chat
    """
    serializer_class = ContractCreateSerializer
    permission_classes = (IsCustomer,)

    @extend_schema(request=ContractCreateRequest, responses={400: BadRequestSerializer, 200: ContractCreateResponse})
    def create(self, request: Request, *args, **kwargs) -> Response:
        """handler for create user"""
        serializer: serializers.Serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'contract_id': serializer.instance.id}, status=status.HTTP_201_CREATED, headers=headers)


class ContractView(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    View for get/set/delete chat
    """
    queryset = Contract.objects.all()
    permission_classes = (IsChatParticipant,)

    action_serializers = {
        'retrieve': ContractDetailSerializer,
        'list': ContractListSerializer
    }

    def get_queryset(self):
        queryset = super(ContractView, self).get_queryset()
        return queryset.filter(Q(customer__id=self.request.user.id) | Q(contractor__id=self.request.user.id))

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(ContractView, self).get_serializer_class()

    @extend_schema(responses={400: BadRequestSerializer, 200: ContractDetailResponse})
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """handler for create user"""
        serializer = self.get_serializer(instance=self.get_object())
        return Response(serializer.data)

    @extend_schema(responses={400: BadRequestSerializer, 200: ContractListResponse})
    def list(self, request: Request, *args, **kwargs) -> Response:
        """handler for create user"""
        queryset: QuerySet = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data)


class CommitCreateView(mixins.CreateModelMixin, GenericViewSet):
    """
    View for get/set/delete chat
    """
    serializer_class = CommitCreateSerializer
    permission_classes = (IsCustomer,)

    @extend_schema(request=CommitCreateRequest, responses={400: BadRequestSerializer, 200: CommitCreateResponse})
    def create(self, request: Request, *args, **kwargs) -> Response:
        """handler for create user"""
        serializer: serializers.Serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'comment_id': serializer.instance.id}, status=status.HTTP_201_CREATED, headers=headers)


class CommitView(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, GenericViewSet):
    """
    View for get/set/delete chat
    """
    queryset = Commit.objects.all()
    permission_classes = (IsChatParticipant,)

    action_serializers = {
        'list': CommitDetailSerializer,
        'retrieve': CommitListSerializer,
        'update': CommitDetailSerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(CommitView, self).get_serializer_class()

    def get_queryset(self):
        queryset = super(CommitView, self).get_queryset()
        return queryset.filter(Q(customer__id=self.request.user.id) | Q(contractor__id=self.request.user.id))

    @extend_schema(request=CommitUpdateRequest, responses={400: BadRequestSerializer, 200: CommitDetailSerializer})
    def update(self, request: Request, *args, **kwargs) -> Response:
        """handler for create user"""
        serializer = self.get_serializer(instance=self.get_object(), data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @extend_schema(responses={400: BadRequestSerializer, 200: CommitDetailSerializer})
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """handler for create user"""
        serializer = self.get_serializer(instance=self.get_object(), need_history=True)
        return Response(serializer.data)

    @extend_schema(responses={400: BadRequestSerializer, 200: CommitListSerializer})
    def list(self, request: Request, *args, **kwargs) -> Response:
        """handler for create user"""
        queryset: QuerySet = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data)


class MessageCreateView(mixins.CreateModelMixin, GenericViewSet):
    serializer_class = MessageDetailSerializer

    @extend_schema(request=MessageCreateRequest, responses={400: BadRequestSerializer, 200: MessageCreateResponse})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class MessageView(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    queryset = Message.objects.all()
    action_serializers = {
        'list': MessageListSerializer,
        'retrieve': MessageDetailSerializer
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(MessageView, self).get_serializer_class()
