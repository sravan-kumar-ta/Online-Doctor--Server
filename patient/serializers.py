from datetime import datetime, timedelta

from rest_framework import serializers

from blog.serializers import UserSerializer
from doctor.models import Doctors
from patient.models import Appointments


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


class DoctorAppSerializer(serializers.ModelSerializer):
    details = UserSerializer()

    class Meta:
        model = Doctors
        fields = ('id', 'specialized_in', 'charge', 'details')
        depth = 2


class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorAppSerializer(read_only=True)
    patient = UserSerializer(read_only=True)

    class Meta:
        model = Appointments
        fields = '__all__'
        depth = 2

    def to_internal_value(self, data):
        mutable_data = data.copy()

        # Convert the time from the frontend to the expected format
        time = datetime.strptime(mutable_data['time'], "%I:%M %p")
        # add the values to the fields before validate
        mutable_data['time'] = time.strftime("%H:%M:%S")

        self.context['doctor'] = mutable_data['doctor']
        return super().to_internal_value(mutable_data)

    def create(self, validated_data):
        date = validated_data['date']
        time = validated_data['time']
        date_time = datetime.combine(date, time)

        validated_data['patient'] = self.context['request'].user
        validated_data['doctor'] = Doctors.objects.get(id=self.context['doctor'])
        validated_data['date_time_start'] = date_time
        validated_data['date_time_end'] = date_time + timedelta(minutes=30)

        return Appointments.objects.create(**validated_data)
