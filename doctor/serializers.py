from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers

from blog.serializers import UserSerializer
from doctor.models import Specialities, Doctors


class SpecialitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialities
        fields = '__all__'


class DoctorSerializer(serializers.ModelSerializer):
    details = UserSerializer(read_only=True)

    class Meta:
        model = Doctors
        fields = '__all__'
        depth = 1

    charge = serializers.IntegerField(validators=[MinValueValidator(100), MaxValueValidator(1500)])

    def update(self, instance, validated_data):
        if self.context.get('special'):
            instance.specialized_in = self.context.get('special')
            instance.save()
        return super().update(instance, validated_data)

    def create(self, validated_data):
        user = self.context.get('user')
        special = self.context.get('special')
        return Doctors.objects.create(details=user, specialized_in=special, **validated_data)
