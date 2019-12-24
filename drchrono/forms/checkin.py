from django import forms
from django.db.models import Q

from drchrono.models import Patient


class CheckinForm(forms.Form):
    first_name = forms.CharField(
        required=True,
        max_length=255,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'First Name'}
        ),
    )
    last_name = forms.CharField(
        required=True,
        max_length=255,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Last Name'}
        ),
    )
    social_security_number = forms.CharField(
        required=False,
        max_length=255,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'pattern': r'\d{3}-\d{2}-\d{4}',
                'placeholder': 'Social Security Number',
            }
        ),
    )

    def clean(self):
        data = super(CheckinForm, self).clean()
        social_security_number = data.get('social_security_number')
        patient = None
        if social_security_number:
            try:
                patient = Patient.objects.get(
                    social_security_number=social_security_number
                )
            except Patient.DoesNotExist:
                pass

        first_name = data.get('first_name')
        last_name = data.get('last_name')

        if first_name and last_name:
            first_name = first_name.lower()
            first_name = first_name.lower()
            patients = Patient.objects.filter(
                Q(social_security_number=None) | Q(social_security_number=''),
                first_name__contains=first_name,
                last_name__icontains=last_name,
            )
            # if we only have one person in the database with the given name
            # but no social security number is set on the patient then let them
            # checkin
            if patients.count() == 1:
                patient = patients.first()

        if patient is None:
            raise forms.ValidationError('Can not find you')

        return {'patient': patient}
