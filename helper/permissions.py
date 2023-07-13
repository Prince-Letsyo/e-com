from rest_framework.permissions import BasePermission
from rest_framework import permissions


class IsVerified(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        verified = False
        if hasattr(user,"emailaddress_set"):
            emailaddresses = user.emailaddress_set.all()
            if emailaddresses:
                for email in emailaddresses:
                    if email.verified and email.primary:
                        verified = True 
                        break
            
        return bool(user and user.is_authenticated and verified == True)


