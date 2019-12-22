from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.views import View
from social_django.models import UserSocialAuth

from drchrono.endpoints import DoctorEndpoint
from drchrono.models import Doctor

_PROVIDER = 'drchrono'


class AfterLoginView(View):
    def get(self, request, *args, **kwargs):
        logout = reverse('logout')
        dashboard = reverse('dashboard')

        social_auth = self._get_social_auth(request.user)
        if social_auth is None:
            messages.error(request, _('oauth.error'))
            return redirect(logout)

        doctor_details = self._get_doctor_details(
            social_auth.extra_data['access_token']
        )

        if not doctor_details:
            messages.error(request, _('drchrono.api.error'))
            return redirect(logout)

        Doctor.objects.create_or_update_doctor(social_auth, doctor_details)

        return redirect(dashboard)

    def _get_social_auth(self, user):
        """
        Social Auth module is configured to store our access tokens.
        This dark magic will fetch it for us if we've
        already signed in.
        """
        try:
            return UserSocialAuth.objects.get(provider=_PROVIDER, user=user)
        except (
            UserSocialAuth.DoesNotExist,
            UserSocialAuth.MultipleObjectsReturned,
        ):
            return None

    def _get_doctor_details(self, access_token):
        """
        Use the token we have stored in the DB to make an API request and
        get doctor details. If this succeeds, we've
        proved that the OAuth setup is working
        """
        # We can create an instance of an endpoint resource class, and use
        # it to fetch details

        api = DoctorEndpoint(access_token)
        # Grab the first doctor from the list; normally this would be the
        # whole practice group, but your hackathon
        # account probably only has one doctor in it.
        return next(api.list())
