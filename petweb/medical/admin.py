from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import PetMedicalForm, PetOperationForm, VaccineForm, VaccineInoculationForm, PetSizeForm
from .models import PetMedical, \
    PetSize, \
    PetOperation, \
    Vaccine, \
    VaccineInoculation


class PetMedicalAdmin(BaseUserAdmin):
    add_form = PetMedicalForm
    form = PetMedicalForm

    list_display = ['pk', 'pet']
    list_display_links = ['pet']
    list_filter = ['pet']

    fieldsets = (
        (None, {'fields': ('pet',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('pet',)}),
    )

    ordering = ('-pk',)
    filter_horizontal = ()


class PetSizeAdmin(BaseUserAdmin):
    add_form = PetSizeForm
    form = PetSizeForm

    list_display = ['pk', 'medical', 'created_date']
    list_display_links = ['medical']
    list_filter = ['medical']

    fieldsets = (
        (None, {'fields': ('medical',)}),
        ('size info', {'fields': ('weight', 'chest', 'neck')}),
    )
    add_fieldsets = (
        (None, {'fields': ('medical',)}),
        ('size info', {'fields': ('weight', 'chest', 'neck')}),
    )

    ordering = ('-pk',)
    filter_horizontal = ()


class PetOperationAdmin(BaseUserAdmin):
    add_form = PetOperationForm
    form = PetOperationForm

    list_display = ['pk', 'medical', 'description', 'date']
    list_display_links = ['medical']
    list_filter = ['medical']

    fieldsets = (
        (None, {'fields': ('medical',)}),
        ('operation info', {'fields': ('image', 'description', 'comment')}),
        ('operation date', {'fields': ('date',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('medical',)}),
        ('operation info', {'fields': ('image', 'description', 'comment')}),
        ('operation date', {'fields': ('date',)}),
    )

    ordering = ('-pk',)
    filter_horizontal = ()


class VaccineAdmin(BaseUserAdmin):
    form = VaccineForm
    add_form = VaccineForm

    list_display = ['pk', 'name', 'turn', 'period', 'species']
    list_display_links = ['name']
    list_editable = ['turn', 'period']
    list_filter = ['species', 'name']

    fieldsets = (
        ('species', {'fields': ('species',)}),
        ('vaccine info', {'fields': ('name', 'turn', 'period')}),
    )

    add_fieldsets = (
        ('species', {'fields': ('species',)}),
        ('vaccine info', {'fields': ('name', 'turn', 'period')}),
    )

    ordering = ('-pk',)
    filter_horizontal = ()


class VaccineInoculationAdmin(BaseUserAdmin):
    form = VaccineInoculationForm
    add_form = VaccineInoculationForm

    list_display = ['pk', 'medical', 'vaccine', 'num_of_times', 'inoculated_date', 'hospital', 'is_alarm']
    list_display_links = ['medical']
    list_editable = ['is_alarm']
    list_filter = ['medical', 'vaccine']

    fieldsets = (
        ('medical info', {'fields': ('medical',)}),
        ('inoculate info', {'fields': ('vaccine', 'num_of_times', 'inoculated_date', 'hospital')}),
        ('extra', {'fields': ('is_alarm',)}),
    )

    add_fieldsets = (
        ('medical info', {'fields': ('medical',)}),
        ('inoculate info', {'fields': ('vaccine', 'num_of_times', 'inoculated_date', 'hospital')}),
        ('extra', {'fields': ('is_alarm',)}),
    )

    ordering = ('-pk',)
    filter_horizontal = ()


admin.site.register(PetMedical, PetMedicalAdmin)
admin.site.register(PetSize, PetSizeAdmin)
admin.site.register(PetOperation, PetOperationAdmin)
admin.site.register(Vaccine, VaccineAdmin)
admin.site.register(VaccineInoculation, VaccineInoculationAdmin)
