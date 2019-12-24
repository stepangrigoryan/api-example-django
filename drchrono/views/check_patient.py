import logging

from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView, UpdateView

from drchrono.decorators import doctor_login_required
from drchrono.forms.checkin import CheckinForm
from drchrono.models import Patient

logger = logging.getLogger()


@method_decorator(doctor_login_required, name='dispatch')
class CheckinPatientView(UpdateView):
    form_class = CheckinForm
    template_name = 'drchrono/checkin.html'

    # def get_success_url(self):
    #     return reverse()

    def get_object(self, queryset=None):
        return get_object_or_404(
            Patient,
            id=self.kwargs['patient_id'],
            doctor_id=self.request.doctor.id,
        )
