from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # read only는 항상 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.owner == request.user