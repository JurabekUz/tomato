from rest_framework import permissions


# class UsersPermission(permissions.BasePermission):
#
#     def has_permission(self, request, view):
#         perm = False
#         if request.user.is_authenticated:
#             if request.method in permissions.SAFE_METHODS or request.user.role == UserRoles.ADMIN:
#                 perm = True
#         return perm
