from django.db import models

from account.models import CustomUser


class Specialities(models.Model):
    title = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.title


class Doctors(models.Model):
    details = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='doctor')
    profile_image = models.ImageField(upload_to='images/doctors', null=True)
    specialized_in = models.ForeignKey(Specialities, on_delete=models.CASCADE)
    charge = models.PositiveIntegerField()
    paypal_account = models.EmailField(max_length=70)

    sun_start = models.TimeField(null=True, blank=True)
    sun_end = models.TimeField(null=True, blank=True)

    mon_start = models.TimeField(null=True, blank=True)
    mon_end = models.TimeField(null=True, blank=True)

    tue_start = models.TimeField(null=True, blank=True)
    tue_end = models.TimeField(null=True, blank=True)

    wed_start = models.TimeField(null=True, blank=True)
    wed_end = models.TimeField(null=True, blank=True)

    thu_start = models.TimeField(null=True, blank=True)
    thu_end = models.TimeField(null=True, blank=True)

    fri_start = models.TimeField(null=True, blank=True)
    fri_end = models.TimeField(null=True, blank=True)

    sat_start = models.TimeField(null=True, blank=True)
    sat_end = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.details.username
