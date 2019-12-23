from django.contrib.auth import logout
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View


class LogoutView(View):
    def get(self, request):
        logout(request)

        return redirect(reverse('home'))
