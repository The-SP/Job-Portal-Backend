from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied, NotAuthenticated


class IsSeeker(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated("You must be authenticated to access this content.")
        if request.user.is_employer:
            raise PermissionDenied(
                "You are not authorized to access this content as an Employer."
            )
        return True


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:  # Safe=GET
            return True
        # Check if the obj has any resume set and Allow write permission to owner only
        if not obj.resume_set.exists() or obj.resume_set.first().user != request.user:
            raise PermissionDenied(
                detail="You are not the owner of this resume object."
            )
        return True


class IsEmployer(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            raise NotAuthenticated("You must be authenticated to access this content.")
        if not request.user.is_employer:
            raise PermissionDenied(
                "You are not authorized to access this content. You must be an Employer."
            )
        return True


class IsJobOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow edit permission to owner only
        if obj.posted_by != request.user:
            raise PermissionDenied(detail="You are not the owner of this job object.")
        return True


# # Allow the owner of the job to view its job-applications
# class IsHiringManager(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if obj.job.posted_by != request.user:
#             raise PermissionDenied(detail="You are not the owner of this job object.")
#         return True


class IsApplicationOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user != request.user:
            raise PermissionDenied(detail="You are not the owner of this job-application.")
        return True