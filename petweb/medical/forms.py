from django import forms

from account.models import Pet
from .models import PetMedical, PetOperation, Vaccine, VaccineInoculation, PetSize


class PetMedicalForm(forms.ModelForm):
    class Meta:
        model = PetMedical
        fields = (
            'pet',
        )


class PetSizeForm(forms.ModelForm):
    class Meta:
        model = PetSize
        fields = (
            'medical',
            'weight',
            'chest',
            'neck',
        )


class PetOperationForm(forms.ModelForm):
    class Meta:
        model = PetOperation
        fields = (
            'medical',
            'image',
            'description',
            'comment',
            'date',
        )


class VaccineForm(forms.ModelForm):
    class Meta:
        model = Vaccine
        fields = (
            'species',
            'name',
            'turn',
            'period',
        )


class VaccineInoculationForm(forms.ModelForm):
    class Meta:
        model = VaccineInoculation
        fields = (
            'medical',
            'vaccine',
            'num_of_times',
            'inoculated_date',
            'hospital',
            'is_alarm',
        )
