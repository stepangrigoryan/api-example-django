from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    Home page shows the login box if the user is not logged in, otherwise
    takes them to the login page.
    """

    template_name = 'drchrono/home.html'

    def get(self, request, *args, **kwargs):
        if request.doctor:
            return redirect(reverse('dashboard'))
        return super(HomeView, self).get(request, *args, **kwargs)
