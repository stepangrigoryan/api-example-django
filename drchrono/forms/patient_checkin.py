from django import forms
from django.db import transaction
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from drchrono.endpoints import PatientEndpoint
from drchrono.models import Patient


class PatientCheckinForm(forms.ModelForm):
    social_security_number = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'pattern': r'\d{3}-\d{2}-\d{4}',
                'placeholder': '123-34-5678',
            }
        ),
    )

    date_of_birth = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(attrs={'type': 'date'}),
    )

    class Meta:
        model = Patient
        fields = (
            'first_name',
            'last_name',
            'social_security_number',
            'race',
            'ethnicity',
            'date_of_birth',
        )

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')
        if not date_of_birth:
            return None

        return date_of_birth

    def clean(self):
        data = super(PatientCheckinForm, self).clean()
        appointment = (
            self.instance.appointments.for_today(self.instance.doctor)
            .order_by('scheduled_time')
            .first()
        )

        if not appointment:
            raise forms.ValidationError(_('checkin.appointment_missing'))

        data['appointment'] = appointment

        return data

    @transaction.atomic
    def save(self, commit=True):
        appointment = self.cleaned_data.pop('appointment')
        appointment.checked_in_at = now()
        appointment.save()
        instance = super(PatientCheckinForm, self).save(commit=commit)
        api = PatientEndpoint(instance.doctor.token)
        data = {
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'social_security_number': instance.social_security_number,
            'race': instance.race,
            'ethnicity': instance.ethnicity,
            'date_of_birth': instance.date_of_birth,
        }
        api.update(instance.drchrono_id, data=data)
