from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth.models import User, Group

class ForManagerOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method !='GET' :
            return request.user.groups.filter(name='manager').exists()
        else:
            return True

class is_manager(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='manager').exists()

class is_coustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='coustomer').exists()
       