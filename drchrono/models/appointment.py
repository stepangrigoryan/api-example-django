from django.db import models
from django.utils.timezone import now

from drchrono.models.base_model import BaseModel


class AppointmentQuerySet(models.QuerySet):
    def for_today(self, doctor):
        date = now().astimezone(doctor.timezone_object).date()
        return self.filter(scheduled_time__date=date, doctor=doctor)


class AppointmentManager(models.Manager):
    def get_queryset(self):
        return AppointmentQuerySet(self.model, using=self._db)

    def for_today(self, doctor):
        return self.get_queryset().for_today(doctor)


class Appointment(BaseModel):
    drchrono_id = models.IntegerField(unique=True)
    patient = models.ForeignKey('drchrono.Patient', related_name='appointments')
    doctor = models.ForeignKey('drchrono.Doctor', related_name='appointments')
    scheduled_time = models.DateTimeField()
    duration = models.IntegerField()
    checked_in_at = models.DateTimeField(null=True, blank=True)
    seen_at = models.DateTimeField(null=True, blank=True)
    time_waited = models.FloatField(null=True, blank=True)
    objects = AppointmentManager()

    def __unicode__(self):
        return 'Appointment for {0} with doctor {1}'.format(
            self.patient, self.doctor
        )

    @property
    def status(self):
        if not self.checked_in_at:
            return 'Not Checked In'
        if not self.seen_at:
            return 'Waiting to be admitted'

        return 'Appointment Finished'
