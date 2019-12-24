from django.db import models

from drchrono.models.base_model import BaseModel


class Patient(BaseModel):
    drchrono_id = models.IntegerField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    social_security_number = models.CharField(
        max_length=20, null=True, blank=True
    )
    race = models.CharField(max_length=255, null=True, blank=True)
    ethnicity = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    doctor = models.ForeignKey('drchrono.Doctor', related_name='patients')

    def __unicode__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)
