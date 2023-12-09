from typing import Optional, Iterable

from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.utils.serializer_helpers import ReturnDict

from chats.models import Commit, Message, Contract, Attachments, CommitTypes
from users.models import UserTypes

User = get_user_model()


def check_sender_type(user: User):
    if getattr(user, 'user_type').lower() != UserTypes.CUSTOMER:
        raise ValidationError(f'Only "customer" user can create a commit\n'
                              f'(excepted: {UserTypes.CUSTOMER}, got {getattr(user, "user_type")})')


def check_contractor_existence(contractor_id: Optional[int]) -> Optional[User]:
    contractor = get_object_or_404(User, pk=contractor_id)
    if contractor.user_type.lower() != UserTypes.CONTRACTOR.lower():
        raise ValidationError(dict(contractor=f'must be a {UserTypes.CONTRACTOR.lower()}'))
    return contractor


def check_contract_existence(pk: Optional[int]) -> Optional[User]:
    return get_object_or_404(Contract, pk=pk)


def check_fields_contain(obj: dict, fields: Iterable):
    for field in fields:
        if obj.get(field) is None:
            raise ValidationError({field: f"The field {field} is required"})


class MessageDetailSerializer(serializers.ModelSerializer):

    @property
    def data(self):
        ret = super(MessageDetailSerializer, self).data
        if not isinstance(self.instance, Message):
            ret['sender'] = getattr(self.context['request'].user, 'id')
        return ReturnDict(ret, serializer=self)

    class Meta:
        model = Message
        fields = ('text', 'contract')


class MessageListSerializer(serializers.ListSerializer):
    child = MessageDetailSerializer()

    @property
    def data(self):
        ret = super(MessageListSerializer, self).data
        if not isinstance(self.instance, Message):
            ret['sender'] = getattr(self.context['request'].user, 'id')
        return ReturnDict(ret, serializer=self)

    class Meta:
        model = Message
        fields = ('text', 'contract')


class CommitCreateSerializer(serializers.ModelSerializer):

    def is_valid(self, *, raise_exception=False):
        user = self.context['request'].user

        check_fields_contain(self.initial_data, ('contract_id', 'current_solution'))
        # check_sender_type(user)
        contract = check_contract_existence(self.initial_data.get('contract_id'))
        prev_commit: Commit = contract.commits.last()
        if prev_commit:
            prev_commit.status = CommitTypes.FINISHED
            prev_commit.save()

        self.initial_data['status'] = CommitTypes.PROCESSED
        self.initial_data['parent'] = prev_commit or None
        self.initial_data['sender'] = user

        solution = {}
        for field_name, passed_value in self.initial_data['current_solution'].items():
            if prev_commit:
                if prev_commit.current_solution.get(field_name, {}).get('value') == passed_value:
                    solution[field_name] = prev_commit.current_solution[field_name]
                    continue
            solution[field_name] = {
                'value': passed_value,
                'history': [passed_value] + (prev_commit.current_solution.get(field_name, {}).get('history', []) if prev_commit else []),
                'comments': []  # {"sender": "comment"}
            }
        self.initial_data['current_solution'] = solution

        return super(CommitCreateSerializer, self).is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        return super(CommitCreateSerializer, self).create(self.initial_data)

    class Meta:
        model = Commit
        fields = ('current_solution',)


class CommitDetailSerializer(serializers.ModelSerializer):

    @property
    def data(self):
        ret = super(CommitDetailSerializer, self).data
        if ret['attachments']:
            ret['attachments'] = Attachments.objects.filter(pk__in=ret['attachments']).all()
        ret['messages'] = MessageDetailSerializer(self.instance.messages.all(), many=True).data
        return ReturnDict(ret, serializer=self)

    def is_valid(self, *, raise_exception=False):
        if self.context['view'].action == 'update':
            self.instance: Commit
            if self.instance != self.instance.contract.commits.last():
                raise ValidationError("You can add comments only for a last commit")
            for field_name, comment in self.initial_data.get('current_solution', {}).items():
                if self.instance.current_solution.get(field_name) is None:
                    raise ValidationError("You can't add comments to non-existent filed")
        return super(CommitDetailSerializer, self).is_valid(raise_exception=raise_exception)

    def update(self, instance, validated_data):
        # current_solution scheme is "current_solution": {"field_name": "comment", ...}
        self.instance: Commit
        for filed_name, comment in validated_data.get('current_solution', {}).items():
            if not isinstance(self.instance.current_solution.get(filed_name), dict):
                self.instance.current_solution[filed_name] = {}
            self.instance.current_solution[filed_name]['comments'] = self.instance.current_solution[filed_name].get(
                'comments', []) + [comment]
        self.instance.save()
        return self.instance

    def to_representation(self, instance):
        data = super(CommitDetailSerializer, self).to_representation(instance)
        if isinstance(instance, Commit):
            data['messages'] = MessageDetailSerializer(instance.messages.all(), many=True).data
            if data['attachments']:
                data['attachments'] = Attachments.objects.filter(pk__in=data['attachments']).all()
        return data

    class Meta:
        model = Commit
        fields = ('current_solution', 'status', 'attachments')
        extra_kwargs = {
            'status': {'required': False},
            'attachments': {'required': False},
        }


class CommitListSerializer(serializers.ListSerializer):
    child = CommitDetailSerializer()

    def to_representation(self, data):
        return self.child.to_representation(data)

    class Meta:
        model = Commit
        fields = ('current_solution', 'status', 'attachments')


class ContractCreateSerializer(serializers.ModelSerializer):

    def is_valid(self, *, raise_exception=False):
        user = self.context['request'].user

        check_sender_type(user)
        contractor = check_contractor_existence(self.initial_data.get('contractor'))

        self.initial_data['customer_id'] = user.id
        self.initial_data['contractor_id'] = contractor.id
        self.initial_data['contractor'] = contractor

        return super(ContractCreateSerializer, self).is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        return super(ContractCreateSerializer, self).create(validated_data=self.initial_data)

    class Meta:
        model = Contract
        fields = ('solution',)


class ContractDetailSerializer(serializers.ModelSerializer):
    def __init__(self, **kwargs):
        self.is_detail = kwargs.pop("is_detail", True)
        super(ContractDetailSerializer, self).__init__(**kwargs)

    @property
    def data(self):
        self.instance: Contract
        other = self.instance.contractor if self.context[
                                                'request'].user == self.instance.customer else self.instance.customer

        ret = {
            'id': self.instance.id, 'name': f'{other.company}',
            'image': other.image if other.image else "",
        }

        if self.is_detail:
            ret |= {
                'commits': CommitDetailSerializer(self.instance.commits.all(), many=True).data,
            }

        return ReturnDict(ret, serializer=self)

    def to_representation(self, instance):
        self.instance = instance
        return self.data

    class Meta:
        model = Contract
        fields = ('solution',)


class ContractListSerializer(serializers.ListSerializer):
    child = ContractDetailSerializer(is_detail=False)

    def to_representation(self, data):
        return self.child.to_representation(data)

    class Meta:
        model = Contract
        fields = ('solution',)
