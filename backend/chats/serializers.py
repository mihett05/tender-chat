from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.utils.serializer_helpers import ReturnDict

from chats.models import Commit, Message, Contract, Attachments, CommitTypes
from users.models import UserTypes

User = get_user_model()


class MessageDetailSerializer(serializers.ModelSerializer):

    @property
    def data(self):
        ret = super(MessageDetailSerializer, self).data
        if not isinstance(self.instance, Message):
            ret['sender'] = getattr(self.context['request'].user, 'id')
        return ret

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
        return ret

    class Meta:
        model = Message
        fields = ('text', 'contract')


class CommitCreateSerializer(serializers.ModelSerializer):

    def is_valid(self, *, raise_exception=False):
        user = self.context['request'].user
        if getattr(user, 'user_type').lower() != UserTypes.CUSTOMER:
            raise ValidationError(f'Only "customer" user can create a commit\n'
                                  f'(excepted: {UserTypes.CUSTOMER}, got {getattr(user, "user_type")})')

        self.instance: Commit
        contract = Contract.objects.filter(pk=self.initial_data['contract_id']).first()

        self.initial_data['status'] = CommitTypes.PROCESSED
        self.initial_data['parent'] = contract.commits.last() or None
        self.initial_data['sender'] = user.id

        solution = {}
        for filed_name, passed_value in self.initial_data['current_solution'].items():
            solution[filed_name] = {
                'value': passed_value,
                'history': [passed_value],
                'comments': []  # {"sender": "comment"}
            }
        self.initial_data['solution'] = solution

        return super(CommitCreateSerializer, self).is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        print(validated_data)
        obj = self.Meta.model.objects.create(**validated_data)
        print(obj, type(obj), obj.__dict__)
        obj.save()
        # return super(CommitCreateSerializer, self).create(validated_data)

    class Meta:
        model = Commit
        fields = ('current_solution',)


class CommitDetailSerializer(serializers.ModelSerializer):

    @property
    def data(self):
        ret = super(CommitDetailSerializer, self).data
        ret['attachments'] = Attachments.objects.filter(pk__in=ret['attachments']).all()
        return ret

    def update(self, instance, validated_data):
        # current_solution scheme is "current_solution": {"field_name": "comment", ...}
        self.instance: Commit

        for filed_name, comment in validated_data.items():
            self.instance.current_solution[filed_name] = {
                "value": self.instance.current_solution.get(filed_name, ""),
                "history": self.instance.current_solution.get(filed_name, dict()).get('history', []),
                "comments": self.instance.current_solution.get(filed_name, dict()).get('comments', []) + [comment]
            }

    def to_representation(self, instance):
        self.instance = instance
        return self.data

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
        if getattr(user, 'user_type').lower() != UserTypes.CUSTOMER:
            raise ValidationError(f'Only "customer" user can create a commit\n'
                                  f'(excepted: {UserTypes.CUSTOMER}, got {getattr(user, "user_type")})')

        self.initial_data['customer'] = user.id

        return super(ContractCreateSerializer, self).is_valid(raise_exception=raise_exception)

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
                'messages': MessageDetailSerializer(self.instance.messages.all(), many=True).data,
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
