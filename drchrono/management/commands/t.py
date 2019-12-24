from django.core.management.base import BaseCommand
from social_django.models import UserSocialAuth

from drchrono.endpoints import PatientEndpoint


class Command(BaseCommand):
    def handle(self, *args, **options):
        patient_endpoint = PatientEndpoint(
            UserSocialAuth.objects.first().extra_data['access_token']
        )
        patients = patient_endpoint.list()
        for patient in patients:
            print(patient)
