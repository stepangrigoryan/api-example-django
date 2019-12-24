import logging

from django.db.models import Avg
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.generic import TemplateView

from drchrono.decorators import doctor_login_required
from drchrono.models import Appointment

logger = logging.getLogger()


@method_decorator(doctor_login_required, name='dispatch')
class DashboardView(TemplateView):
    """
    The doctor can see what appointments they have today.
    """

    template_name = 'drchrono/dashboard.html'

    def get_context_data(self, **kwargs):
        kwargs = super(DashboardView, self).get_context_data(**kwargs)
        kwargs['appointments'] = (
            Appointment.objects.for_today(self.request.doctor)
            .order_by('-scheduled_time')
            .select_related('patient')
        )
        kwargs['average_time_waited'] = (
            self.request.doctor.appointments.exclude(
                time_waited=None
            ).aggregate(average_time_waited=Avg('time_waited'))
        )['average_time_waited'] / 60.0
        kwargs['latest_update'] = now()

        return kwargs
