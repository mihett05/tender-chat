from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from chats.models import Contract
from users.models import UserTypes


class IsChatParticipant(permissions.IsAuthenticated):
    def has_object_permission(self, request: Request, view: APIView, obj: Contract):
        return request.user == obj.customer or request.user == obj.contractor


class IsCustomer(permissions.IsAuthenticated):
    def has_permission(self, request: Request, view: APIView):
        return request.user.user_type == UserTypes.CUSTOMER
