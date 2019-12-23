from django.utils.deprecation import MiddlewareMixin

from drchrono.models import Doctor


class DoctorMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.doctor = None
        if request.user.is_authenticated:
            request.doctor = Doctor.objects.filter(
                social_auth__user=request.user
            ).first()
