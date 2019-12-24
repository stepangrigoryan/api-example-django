from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import LogoutView

from drchrono.views.after_login import AfterLoginView
from drchrono.views.checkin import CheckinView
from drchrono.views.dashboard import DashboardView
from drchrono.views.home import HomeView
from drchrono.views.webhook import WebhookView

admin.autodiscover()

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^webhook/$', WebhookView.as_view(), name='webhook'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^checkin/$', CheckinView.as_view(), name='checkin',),
    url(
        r'^checkin/(?P<patient_id>[0-9A-Fa-f-]+)/$',
        CheckinView.as_view(),
        name='checkin_patient',
    ),
    url(r'^dashboard/$', DashboardView.as_view(), name='dashboard',),
    url(r'^after-login/$', AfterLoginView.as_view(), name='post_login',),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]
