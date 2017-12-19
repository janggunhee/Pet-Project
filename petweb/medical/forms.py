from django import forms

from account.models import Pet
from .models import PetMedical, PetOperation, Vaccine


class PetMedicalForm(forms.ModelForm):
    class Meta:
        model = PetMedical
        fields = (
            'pet',
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
