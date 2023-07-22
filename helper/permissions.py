from rest_framework.permissions import BasePermission


class IsVerified(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        verified = False
        if hasattr(user, "emailaddress_set"):
            emailaddresses = user.emailaddress_set.all()
            if emailaddresses:
                for email in emailaddresses:
                    if email.verified and email.primary:
                        verified = True
                        break

        return bool(user and user.is_authenticated and verified == True)


class IsVerifiedSiteOwner(IsVerified):
    def has_permission(self, request, view):
        has_site = False
        user = request.user
        site_owners = user.groups.filter(name="Site Owners")
        if site_owners.exists():
            has_site = True

        return bool(has_site and super().has_permission(request, view))
