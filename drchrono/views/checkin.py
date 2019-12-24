import logging

from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import FormView

from drchrono.decorators import doctor_login_required
from drchrono.forms.checkin import CheckinForm

logger = logging.getLogger()


@method_decorator(doctor_login_required, name='dispatch')
class CheckinView(FormView):
    form_class = CheckinForm
    template_name = 'drchrono/checkin.html'

    def form_valid(self, form):
        return HttpResponseRedirect(
            reverse('patient_checkin', args=(form.cleaned_data['patient'].id,))
        )
