from django import forms

from drchrono.models import Doctor, Patient

EVENT_CHOICES = (
    'APPOINTMENT_CREATE',
    'APPOINTMENT_DELETE',
    'APPOINTMENT_MODIFY',
    'PATIENT_CREATE',
    'PATIENT_MODIFY',
)


class WebhookPatientForm(forms.Form):
    id = forms.IntegerField()
    doctor = forms.IntegerField()
    social_security_number = forms.CharField(required=False)
    first_name = forms.CharField()
    last_name = forms.CharField()
    race = forms.CharField(required=False)
    ethnicity = forms.CharField(required=False)
    date_of_birth = forms.DateField(required=False)

    def clean_doctor(self):
        doctor = self.cleaned_data.get('doctor')
        if doctor:
            try:
                doctor = Doctor.objects.get(drchrono_id=doctor)
            except Doctor.DoesNotExist:
                raise forms.ValidationError('doctor does not exist')
        return doctor

    def clean(self):
        cleaned_data = super(WebhookPatientForm, self).clean()
        cleaned_data['drchrono_id'] = cleaned_data['id']
        cleaned_data.pop('id')

    def save(self):
        data = self.cleaned_data
        doctor = data.pop('doctor')
        patient, _ = Patient.objects.update_or_create(
            doctor=doctor, defaults=data
        )
        return patient
