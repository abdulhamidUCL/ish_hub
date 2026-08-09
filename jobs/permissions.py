from rest_framework.permissions import BasePermission


class IsEmployer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.profile.role == "employer"
        )

class IsSeeker(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.profile.role == "seeker"
        )

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsCompanyOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user

class IsApplicationOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.user == request.user
            or obj.job.company.owner == request.user
        )

class IsJobOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.company.owner == request.user

class IsApplicationEmployer(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.job.company.owner == request.user