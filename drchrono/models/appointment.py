from django.db import models

from drchrono.models.base_model import BaseModel


class Appointment(BaseModel):
    drchrono_id = models.IntegerField(unique=True)
    patient = models.ForeignKey('drchrono.Patient', related_name='appointments')
    doctor = models.ForeignKey('drchrono.Doctor', related_name='appointments')

    def __unicode__(self):
        return 'Appointment for {0} with doctor {1}'.format(
            self.patient, self.doctor
        )
