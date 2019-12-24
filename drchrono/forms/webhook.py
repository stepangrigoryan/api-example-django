from django import forms
from django.utils.dateparse import parse_datetime

from drchrono.models import Doctor, Patient
from drchrono.models.appointment import Appointment

EVENT_CHOICES = (
    'APPOINTMENT_CREATE',
    'APPOINTMENT_DELETE',
    'APPOINTMENT_MODIFY',
    'PATIENT_CREATE',
    'PATIENT_MODIFY',
)


class WebhookAppointmentBaseForm(forms.Form):
    def get_object(self, model_class, field, data):
        object_id = self.cleaned_data.get(field)
        if not object_id:
            return object_id

        try:
            obj = model_class.objects.get(drchrono_id=object_id)
        except model_class.DoesNotExist:
            raise forms.ValidationError('Associated object does not exist')
        return obj


class WebhookPatientForm(WebhookAppointmentBaseForm):
    id = forms.IntegerField()
    doctor = forms.IntegerField()
    social_security_number = forms.CharField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()
    race = forms.CharField(required=False)
    ethnicity = forms.CharField(required=False)
    date_of_birth = forms.DateField(required=False)

    def clean_doctor(self):
        return self.get_object(Doctor, 'doctor', self.cleaned_data)

    def save(self):
        data = self.cleaned_data
        drchrono_id = data.pop('id')
        patient, _ = Patient.objects.update_or_create(
            drchrono_id=drchrono_id, defaults=data
        )
        return patient


class WebhookAppointmentForm(WebhookAppointmentBaseForm):
    id = forms.IntegerField()
    doctor = forms.IntegerField()
    patient = forms.IntegerField()
    scheduled_time = forms.CharField(required=False)
    duration = forms.IntegerField()

    def clean_doctor(self):
        return self.get_object(Doctor, 'doctor', self.cleaned_data)

    def clean_patient(self):
        return self.get_object(Patient, 'patient', self.cleaned_data)

    def clean(self):
        data = super(WebhookAppointmentForm, self).clean()
        scheduled_time = parse_datetime(data['scheduled_time'])
        data['scheduled_time'] = data['doctor'].timezone_object.localize(
            scheduled_time
        )

        return data

    def save(self):
        data = self.cleaned_data
        drchrono_id = data.pop('id')
        appointment, _ = Appointment.objects.update_or_create(
            drchrono_id=drchrono_id, defaults=data
        )
        return appointment


EVENT_MAPPING = {
    'APPOINTMENT_CREATE': WebhookAppointmentForm,
    'APPOINTMENT_MODIFY': WebhookAppointmentForm,
    'PATIENT_CREATE': WebhookPatientForm,
    'PATIENT_MODIFY': WebhookPatientForm,
}


def get_form_class_for_event(event):
    return EVENT_MAPPING.get(event)
