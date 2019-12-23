from django.db import models

from drchrono.models.base_model import BaseModel


class Patient(BaseModel):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    ssn = models.CharField(max_length=20)

    def __unicode__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)
