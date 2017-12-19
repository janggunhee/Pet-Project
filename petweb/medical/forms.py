from django import forms

from account.models import Pet
from .models import PetMedical


class PetMedicalCreateForm(forms.ModelForm):
    pet = forms.ModelChoiceField(
        label='Pet',
        queryset=Pet.objects.all(),
        required=True,
    )


class PetMedicalChangeForm(forms.ModelForm):
    class Meta:
        model = PetMedical
        fields = (
            'pet',
        )
