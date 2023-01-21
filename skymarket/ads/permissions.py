from rest_framework.permissions import BasePermission

from users.models import UserRoles


class EditPermission(BasePermission):
    message = "only the administrator can edit other people's ads"

    def has_permission(self, request, view):
        print(request.method)
        print(view.get_object())
        print(request.user.role)
        print(UserRoles.ADMIN)
        print(request.user == view.get_object().author \
                or request.user.role == UserRoles.ADMIN\
                or request.method == 'GET')
        if request.user == view.get_object().author \
                or request.user.role == UserRoles.ADMIN\
                or request.method == 'GET':
            return True
        return False
