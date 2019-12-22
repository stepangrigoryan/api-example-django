import pprint

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from social_django.models import UserSocialAuth
from django.utils.translation import gettext_lazy as _
from drchrono.endpoints import DoctorEndpoint
from drchrono.models import Doctor

_PROVIDER = 'drchrono'


_('hello.there')


class SetupView(TemplateView):
    """
    The beginning of the OAuth sign-in flow. Logs a user into the kiosk, and saves the token.
    """

    template_name = 'login.html'


class DoctorWelcome(TemplateView):
    """
    The doctor can see what appointments they have today.
    """

    template_name = 'doctor_welcome.html'

    def get_token(self):
        """
        Social Auth module is configured to store our access tokens.
        This dark magic will fetch it for us if we've
        already signed in.
        """
        oauth_provider = UserSocialAuth.objects.get(provider='drchrono')
        access_token = oauth_provider.extra_data['access_token']
        return access_token

    def make_api_request(self):
        """
        Use the token we have stored in the DB to make an API request and get
        doctor details. If this succeeds, we've
        proved that the OAuth setup is working
        """
        # We can create an instance of an endpoint resource class, and use it
        # to fetch details
        access_token = self.get_token()
        api = DoctorEndpoint(access_token)
        # Grab the first doctor from the list; normally this would be the whole
        # practice group, but your hackathon
        # account probably only has one doctor in it.
        return next(api.list())

    def get_context_data(self, **kwargs):
        kwargs = super(DoctorWelcome, self).get_context_data(**kwargs)
        # Hit the API using one of the endpoints just to prove that we can
        # If this works, then your oAuth setup is working correctly.
        doctor_details = self.make_api_request()
        s = pprint.pformat(doctor_details)
        kwargs['doctor'] = doctor_details
        kwargs['s'] = s
        return kwargs


class PostLoginView(View):
    def get(self, request, *args, **kwargs):
        message = 'something went wrong'
        home = reverse('home')
        dashboard = reverse('dashboard')

        social_auth = self._get_social_auth(request.user)
        if social_auth is None:
            messages.error(request, message)
            return redirect(home)

        doctor_details = self._get_doctor_details(
            social_auth.extra_data['access_token']
        )

        if not doctor_details:
            messages.error(request, message)
            return redirect(home)

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
