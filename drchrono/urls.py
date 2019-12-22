from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

from drchrono import views
from drchrono.decorators import doctor_login_required

admin.autodiscover()

urlpatterns = [
    url(r'^setup/$', views.SetupView.as_view(), name='home'),
    url(
        r'^welcome/$',
        doctor_login_required(views.DoctorWelcome.as_view()),
        name='dashboard',
    ),
    url(
        r'^post-login/$',
        login_required(views.PostLoginView.as_view()),
        name='post_login',
    ),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
]
