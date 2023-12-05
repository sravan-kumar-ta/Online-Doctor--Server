from django.db import models

from account.models import CustomUser
from doctor.models import Doctors


class Appointments(models.Model):
    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"

    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="app_patient", blank=True)
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, related_name="app_doctor")
    date = models.DateField()
    time = models.TimeField()
    date_time_start = models.DateTimeField(blank=True)
    date_time_end = models.DateTimeField(blank=True)

    def __str__(self):
        return str(self.pk) + ' | ' + str(self.doctor.details.first_name) + ' | ' + str(self.patient.first_name)
