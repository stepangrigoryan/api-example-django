from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils.timezone import now
from social_django.models import UserSocialAuth

from drchrono.endpoints import (
    PatientEndpoint,
    AppointmentEndpoint,
)
from drchrono.forms.webhook import WebhookPatientForm, WebhookAppointmentForm


class Command(BaseCommand):
    def handle(self, *args, **options):
        access_token = UserSocialAuth.objects.first().extra_data['access_token']
        self.load_patients(access_token)
        self.load_appointments(access_token)

    def load_patients(self, access_token):
        patient_endpoint = PatientEndpoint(access_token)
        patients = patient_endpoint.list()
        for data in patients:
            form = WebhookPatientForm(data=data)
            print(form)
            if form.is_valid():
                form.save()
            else:
                print(form.errors)

    def load_appointments(self, access_token):
        api = AppointmentEndpoint(access_token)
        start = (now() - timedelta(days=1)).day
        end = (now() + timedelta(days=1)).day
        appointments = api.list(start=start, end=end)

        for data in appointments:
            form = WebhookAppointmentForm(data=data)
            print(form)
            if form.is_valid():
                form.save()
            else:
                print(form.errors)
