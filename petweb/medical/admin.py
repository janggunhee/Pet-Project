from django.contrib import admin

from medical.models import PetMedical, PetSize, PetVaccine, PetOperation, VaccineInfo

admin.site.register(PetMedical)
admin.site.register(PetSize)
admin.site.register(PetOperation)
admin.site.register(PetVaccine)
admin.site.register(VaccineInfo)
