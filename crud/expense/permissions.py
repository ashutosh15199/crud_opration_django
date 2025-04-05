from rest_framework.permissions import BasePermission

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsManagerUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['manager','user']
    
    def has_object_permission(self, request, view, obj):
        return request.method in['GET','PUT','PATCH'] and obj.user==request.user
