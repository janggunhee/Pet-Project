from django import forms

from account.models import Pet
from .models import PetMedical, Operation, Vaccine, Inoculation, BodySize


class PetMedicalForm(forms.ModelForm):
    class Meta:
        model = PetMedical
        fields = (
            'pet',
        )


class BodySizeForm(forms.ModelForm):
    class Meta:
        model = BodySize
        fields = (
            'medical',
            'goal_weight',
            'current_weight',
            'chest',
            'neck',
        )


class OperationForm(forms.ModelForm):
    class Meta:
        model = Operation
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


class InoculationForm(forms.ModelForm):
    class Meta:
        model = Inoculation
        fields = (
            'medical',
            'vaccine',
            'num_of_times',
            'inoculated_date',
            'hospital',
            'is_alarm',
        )
