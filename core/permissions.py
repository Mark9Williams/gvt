# from rest_framework.permissions import BasePermission


# class IsManager(BasePermission):
#     """Allow access only to users with the manager role."""

#     def has_permission(self, request, view):
#         user = request.user
#         if not user or not user.is_authenticated:
#             return False
#         # assume role field on custom user model
#         return getattr(user, "role", None) == "manager"
