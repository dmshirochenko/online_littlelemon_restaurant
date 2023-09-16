from rest_framework import permissions

class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='Manager').exists())

class IsDeliveryCrew(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='Delivery Crew').exists())

class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.groups.filter(name='Customer').exists())
