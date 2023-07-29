from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


def get_user_model(isSite_user):
    """
    Return the User model that is active in this project.
    """
    try:
        return django_apps.get_model(
            "user.SiteOwner" if not isSite_user else "user.SiteUser",
            require_ready=False,
        )
    except ValueError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "AUTH_USER_MODEL refers to model '%s' that has not been installed"
            % settings.AUTH_USER_MODEL
        )
