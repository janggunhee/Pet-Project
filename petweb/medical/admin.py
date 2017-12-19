from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import PetMedicalCreateForm, PetMedicalChangeForm
from .models import PetMedical, PetSize, PetOperation, Vaccine, VaccineInoculation


class PetMedicalAdmin(BaseUserAdmin):
    add_form = PetMedicalCreateForm
    form = PetMedicalChangeForm
    list_display = ['pk', 'pet']
    list_display_links = ['pet']
    list_filter = ['pet']

    fieldsets = (
        (None, {'fields': ('pet',)}),
    )

    add_fieldsets = (
        (None, {'fields': ('pet',)}),
    )
    ordering = ('pk',)
    filter_horizontal = ()


admin.site.register(PetMedical, PetMedicalAdmin)
admin.site.register(PetSize)
admin.site.register(PetOperation)
admin.site.register(Vaccine)
admin.site.register(VaccineInoculation)
