from django import forms
from django.utils.translation import gettext_lazy as _

from drchrono.models import Patient


class CheckinForm(forms.Form):
    first_name = forms.CharField(
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Joe'}),
    )
    last_name = forms.CharField(
        required=True,
        max_length=255,
        widget=forms.TextInput(attrs={'placeholder': 'Smith'}),
    )
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

    def clean(self):
        data = super(CheckinForm, self).clean()
        social_security_number = data.get('social_security_number')
        patient = None
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        if first_name and last_name:
            first_name = first_name.lower()
            first_name = first_name.lower()
            patients = Patient.objects.filter(
                social_security_number=social_security_number,
                first_name__contains=first_name,
                last_name__icontains=last_name,
            )
            # If we have multiple people with the same name and social then
            # take the first one
            if patients.count() == 1:
                patient = patients.first()

        if patient is None:

            raise forms.ValidationError(_('checkin.patient_not_found'))

        return {'patient': patient}
