from django import forms
from django.utils.timezone import now


class SeePatientForm(forms.Form):
    def __init__(self, appointment, *args, **kargs):
        self.appointment = appointment
        super(SeePatientForm, self).__init__(*args, **kargs)

    def clean(self):
        if self.appointment.seen_at:
            raise forms.ValidationError('Already seen this patient')
        if not self.appointment.checked_in_at:
            raise forms.ValidationError('Patient has not checked in yet')

    def save(self):
        self.appointment.seen_at = now()
        self.appointment.time_waited = (
            self.appointment.seen_at - self.appointment.checked_in_at
        ).seconds
        self.appointment.save()
