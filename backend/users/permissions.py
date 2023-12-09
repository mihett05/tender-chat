from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import APIView

from chats.models import Contract, Commit
from users.models import UserTypes


class IsChatParticipant(permissions.IsAuthenticated):
    def has_object_permission(self, request: Request, view: APIView, obj: Contract):
        if isinstance(obj, Commit):
            obj = obj.contract
        return request.user == obj.customer or request.user == obj.contractor


class IsCustomer(permissions.IsAuthenticated):
    def has_permission(self, request: Request, view: APIView):
        return super(IsCustomer, self).has_permission(request, view) and request.user.user_type == UserTypes.CUSTOMER
