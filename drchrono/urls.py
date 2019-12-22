from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView

import drchrono.views.after_login
import drchrono.views.dashboard
import drchrono.views.home
from drchrono.decorators import doctor_login_required

admin.autodiscover()

urlpatterns = [
    url(r'^$', drchrono.views.home.HomeView.as_view(), name='home'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(
        r'^dashboard/$',
        doctor_login_required(drchrono.views.dashboard.DashboardView.as_view()),
        name='dashboard',
    ),
    url(
        r'^after-login/$',
        login_required(drchrono.views.after_login.AfterLoginView.as_view()),
        name='post_login',
    ),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]
