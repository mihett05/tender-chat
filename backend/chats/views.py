from django.contrib.auth import get_user_model
from django.db.models import QuerySet, Q
from drf_spectacular.utils import extend_schema
from rest_framework import (mixins, status, serializers)
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from authentication.serializers import BadRequestSerializer
from chats.models import Contract, Commit, Message, ContractTypes
from chats.schemes import ContractCreateRequest, ContractCreateResponse, ContractDetailResponse, ContractListResponse, \
    CommitCreateRequest, CommitUpdateRequest, MessageCreateRequest, MessageCreateResponse, CommitCreateResponse
from chats.serializers import (
    ContractCreateSerializer, ContractListSerializer, ContractDetailSerializer,
    CommitCreateSerializer, CommitDetailSerializer, CommitListSerializer,
    MessageDetailSerializer, MessageListSerializer, ContractUpdateSerializer,
)
from users.permissions import IsChatParticipant, IsCustomer

User = get_user_model()


class ContractView(mixins.RetrieveModelMixin,
                   mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    """
    View for get/get list/set/create chat (contract)
    """
    queryset = Contract.objects.all()
    permission_classes = (IsChatParticipant,)

    action_serializers = {
        'retrieve': ContractDetailSerializer,
        'create': ContractCreateSerializer,
        'list': ContractListSerializer,
        'update': ContractUpdateSerializer
    }

    def get_queryset(self):
        queryset = super(ContractView, self).get_queryset()
        return queryset.filter(Q(customer__id=self.request.user.id) | Q(contractor__id=self.request.user.id))

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(ContractView, self).get_serializer_class()

    @extend_schema(request=ContractCreateRequest, responses={400: BadRequestSerializer, 200: ContractCreateResponse})
    def create(self, request: Request, *args, **kwargs) -> Response:
        """handler for create contract"""
        serializer: serializers.Serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'contract_id': serializer.instance.id}, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(responses={400: BadRequestSerializer, 200: ContractDetailResponse})
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """handler for get detail contract"""
        serializer = self.get_serializer(instance=self.get_object())
        return Response(serializer.data)

    @extend_schema(responses={400: BadRequestSerializer, 200: ContractDetailResponse})
    def update(self, request: Request, *args, **kwargs) -> Response:
        """handler for set contract status"""
        return super(ContractView, self).update(request, *args, **kwargs)

    @extend_schema(responses={400: BadRequestSerializer, 200: ContractListResponse})
    def list(self, request: Request, *args, **kwargs) -> Response:
        """handler for create user"""
        queryset: QuerySet = self.get_queryset().filter(not Q(contract_type=ContractTypes.FINISHED))
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data)


class CommitView(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.CreateModelMixin,
                 mixins.ListModelMixin,
                 GenericViewSet):
    """
    View for get/set/delete chat
    """
    queryset = Commit.objects.all()
    permission_classes = (IsChatParticipant,)

    action_serializers = {
        'list': CommitListSerializer,
        'retrieve': CommitDetailSerializer,
        'update': CommitDetailSerializer,
        'create': CommitCreateSerializer,
    }

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(CommitView, self).get_serializer_class()

    def get_queryset(self):
        queryset = super(CommitView, self).get_queryset()
        filter_query = Q(contract__customer__id=self.request.user.id)
        if self.action != 'create':
            filter_query |= Q(contract__contractor__id=self.request.user.id)
        return queryset.filter(filter_query)

    @extend_schema(request=CommitCreateRequest, responses={400: BadRequestSerializer, 200: CommitCreateResponse})
    def create(self, request: Request, *args, **kwargs) -> Response:
        """handler for create user"""
        serializer: serializers.Serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({'commit_id': serializer.instance.id}, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(request=CommitUpdateRequest, responses={400: BadRequestSerializer, 200: CommitDetailSerializer})
    def update(self, request: Request, *args, **kwargs) -> Response:
        """handler for create user"""
        obj: Commit = self.get_object()
        serializer = self.get_serializer(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @extend_schema(responses={400: BadRequestSerializer, 200: CommitDetailSerializer})
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        """handler for create user"""
        serializer = self.get_serializer(instance=self.get_object())
        return Response(serializer.data)

    @extend_schema(responses={400: BadRequestSerializer, 200: CommitListSerializer})
    def list(self, request: Request, *args, **kwargs) -> Response:
        """handler for create user"""
        queryset: QuerySet = self.get_queryset()
        serializer = self.get_serializer(instance=queryset, many=True)
        return Response(serializer.data)


class MessageView(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  GenericViewSet):
    queryset = Message.objects.all()
    action_serializers = {
        'list': MessageDetailSerializer,
        'retrieve': MessageDetailSerializer,
        'create': MessageDetailSerializer,
    }

    @extend_schema(responses={400: BadRequestSerializer, 200: MessageListSerializer})
    def list(self, request: Request, *args, **kwargs) -> Response:
        """handler for create user"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return super(MessageView, self).list(request, *args, **kwargs)

    @extend_schema(request=MessageCreateRequest, responses={400: BadRequestSerializer, 200: MessageCreateResponse})
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(MessageView, self).get_serializer_class()
