from django.contrib import admin

from medical.models import PetMedical, PetSize, PetOperation, Vaccine, VaccineInoculation

admin.site.register(PetMedical)
admin.site.register(PetSize)
admin.site.register(PetOperation)
admin.site.register(Vaccine)
admin.site.register(VaccineInoculation)
