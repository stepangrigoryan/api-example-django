from django.db import models

from drchrono.models.base_model import BaseModel


class DoctorManager(models.Manager):
    def create_or_update_doctor(self, social_auth, data):
        drchrono_id = data['id']

        defaults = {
            'cell_phone': data['cell_phone'],
            'office_phone': data['office_phone'],
            'home_phone': data['home_phone'],
            'email': data['email'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'drchrono_practice_group_id': data['practice_group'],
            'social_auth': social_auth,
        }
        doctor, _ = self.update_or_create(
            drchrono_id=drchrono_id, defaults=defaults
        )

        return doctor


class Doctor(BaseModel):
    cell_phone = models.CharField(max_length=255, blank=True, null=True)
    office_phone = models.CharField(max_length=255, blank=True, null=True)
    home_phone = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    drchrono_id = models.IntegerField(unique=True)
    drchrono_practice_group_id = models.IntegerField()
    social_auth = models.OneToOneField(
        'social_django.UserSocialAuth', models.PROTECT, related_name='doctor')

    objects = DoctorManager()

    def __unicode__(self):
        return '{0} {1}'.format(self.first_name, self.last_name)

    @property
    def phone(self):
        return self.office_phone or self.cell_phone or self.home_phone
