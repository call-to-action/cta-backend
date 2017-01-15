from rest_framework import permissions
from rest_framework.authentication import BasicAuthentication,SessionAuthentication

class IsAdminOrIsSelf(permissions.BasePermission):

    def has_permission(self, request, view):
        return True

