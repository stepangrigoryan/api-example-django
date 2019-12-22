from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test

from drchrono.models import Doctor


def doctor_login_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None
):
    """
    Decorator for views that checks that the user is logged in and the user has
    a valid doctor associated with it, redirecting to the log-in page
    if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: (
            u.is_authenticated
            and Doctor.objects.filter(social_auth__user=u).exists()
        ),
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
