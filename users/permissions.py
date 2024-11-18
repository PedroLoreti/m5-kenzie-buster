from rest_framework import permissions
from users.models import User
from rest_framework.views import Request, View


class IsUserOwner(permissions.BasePermission):

    def has_permission(self, request: Request, view: View):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request: Request, view: View, obj: User):
        if request.user.is_employee:
            return True

        return obj == request.user
