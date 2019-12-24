import logging

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from drchrono.decorators import doctor_login_required
from drchrono.forms.patient_checkin import PatientCheckinForm
from drchrono.models import Patient

logger = logging.getLogger()


@method_decorator(doctor_login_required, name='dispatch')
class PatientCheckinView(UpdateView):
    form_class = PatientCheckinForm
    template_name = 'drchrono/patient_checkin.html'

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Successfully checked in')
        return HttpResponseRedirect(reverse('checkin'))

    def get_object(self, queryset=None):
        return get_object_or_404(
            Patient,
            id=self.kwargs['patient_id'],
            doctor_id=self.request.doctor.id,
        )
