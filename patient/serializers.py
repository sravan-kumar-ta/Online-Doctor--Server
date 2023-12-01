from rest_framework import serializers

from blog.serializers import UserSerializer
from doctor.models import Doctors


class DoctorSerializer(serializers.ModelSerializer):
    details = UserSerializer()

    class Meta:
        model = Doctors
        fields = '__all__'
        depth = 1


class AvailableTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctors
        exclude = ('id', 'details', 'profile_image', 'specialized_in', 'charge', 'paypal_account')
