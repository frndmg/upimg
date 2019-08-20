from rest_framework.permissions import BasePermission

from . import models

class ImageUploadPermission(BasePermission):
    message = 'User does not request this upload link or expired'

    def has_permission(self, req, view):
        token = req.resolver_match.kwargs.get('token')
        try:
            up_token = models.UploadToken.objects.filter(token=token).get()
        except models.UploadToken.DoesNotExist:
            return False

        if req.user != up_token.user:
            return False

        return True
