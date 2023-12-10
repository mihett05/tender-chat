from django.contrib.auth import get_user_model
from rest_framework import serializers

from chats.serializers import CommitDetailSerializer, MessageDetailSerializer

User = get_user_model()


class SolutionItemSchema(serializers.Serializer):
    value = serializers.CharField()
    history = serializers.ListField()
    comments = serializers.ListField()


class ContractCreateRequest(serializers.Serializer):
    solution = serializers.JSONField()


class ContractCreateResponse(serializers.Serializer):
    contract_id = serializers.IntegerField()


class ContractResponse(serializers.Serializer):
    id = serializers.IntegerField()
    image = serializers.ImageField()


class ContractDetailResponse(ContractResponse):
    commits = CommitDetailSerializer


class ContractListResponse(serializers.Serializer):
    contracts = serializers.ListField(child=ContractResponse())


class CommitCreateRequest(serializers.Serializer):
    contract_id = serializers.IntegerField()
    current_solution = serializers.JSONField()


class CommitCreateResponse(serializers.Serializer):
    comment_id = serializers.IntegerField()


class CommitUpdateRequest(serializers.Serializer):
    current_solution = serializers.JSONField()


class MessageCreateRequest(serializers.Serializer):
    text = serializers.CharField()
    contract = serializers.IntegerField()


class MessageCreateResponse(serializers.Serializer):
    text = serializers.CharField()
    contract = serializers.IntegerField()
    sender = serializers.IntegerField()
