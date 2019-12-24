import logging

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from drchrono.decorators import doctor_login_required
from drchrono.forms.see_patient import SeePatientForm
from drchrono.models import Appointment

logger = logging.getLogger()


@method_decorator(doctor_login_required, name='dispatch')
class SeePatientView(FormView):
    form_class = SeePatientForm
    template_name = 'drchrono/dashboard.html'

    def form_invalid(self, form):
        for error in form.errors['__all__']:
            messages.error(self.request, error)
        return HttpResponseRedirect(reverse('dashboard'))

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Successfully set')
        return HttpResponseRedirect(reverse('dashboard'))

    def get_form_kwargs(self):
        kwargs = super(SeePatientView, self).get_form_kwargs()
        appointment = get_object_or_404(
            Appointment,
            id=self.kwargs['appointment_id'],
            doctor_id=self.request.doctor.id,
        )

        kwargs['appointment'] = appointment

        return kwargs
