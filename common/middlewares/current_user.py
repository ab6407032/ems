# Global thread-safe variable
from threading import local
from django.utils.deprecation import MiddlewareMixin

_user = local()


class CurrentUserMiddleware(MiddlewareMixin):
    """
    Middleware which stores request's user into global thread-safe
    variable.
    """

    def process_request(self, request):
        _user.value = request.user

    @staticmethod
    def get_current_user():
        if hasattr(_user, 'value') and _user.value:
            return _user.value


def get_current_user():
    try:
        return _user.value
    except AttributeError:
        return None
