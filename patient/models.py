from django.db import models

from account.models import CustomUser
from doctor.models import Doctors


class Appointments(models.Model):
    class Meta:
        verbose_name = "Appointment"
        verbose_name_plural = "Appointments"

    patient = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="app_patient")
    doctor = models.ForeignKey(Doctors, on_delete=models.CASCADE, related_name="app_doctor")
    date_time_start = models.DateTimeField()
    date_time_end = models.DateTimeField()

    def __str__(self):
        return str(self.pk) + ' | ' + str(self.doctor.details.first_name) + ' | ' + str(self.patient.first_name)
