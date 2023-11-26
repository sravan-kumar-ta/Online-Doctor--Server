from django.contrib import admin
from doctor.models import Doctors, Specialities


# Register your models here.
class DoctorsAdmin(admin.ModelAdmin):
    list_display = ('details', 'specialized_in')


admin.site.register(Specialities)
admin.site.register(Doctors, DoctorsAdmin)
