from datetime import datetime

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor.models import Specialities, Doctors
from doctor.permissions import IsDoctor
from doctor.serializers import SpecialitiesSerializer, DoctorSerializer
from patient.models import Appointments
from patient.serializers import AppointmentSerializer


class SpecialitiesView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SpecialitiesSerializer
    queryset = Specialities.objects.all()


class DoctorDetailsView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]
    serializer_class = DoctorSerializer

    def get(self, request, *args, **kwargs):
        # Retrieve the doctor details for the authenticated user or raise a 404 if not found
        obj = get_object_or_404(Doctors, details=request.user)
        serializer = self.serializer_class(obj)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Check if the user already has a doctor profile
        if Doctors.objects.filter(details=request.user).exists():
            return Response({'message': 'You already created a doctor profile.'}, status=status.HTTP_406_NOT_ACCEPTABLE)

        # Check if 'specialized_in_id' is provided and retrieve the Specialities object
        specialized_in_id = request.data.get('specialized_in')
        if not specialized_in_id:
            return Response({'specialized_in': 'This field is required.'}, status=status.HTTP_400_BAD_REQUEST)
        speciality = get_object_or_404(Specialities, id=specialized_in_id)

        # Create a new doctor profile for the user
        serializer = DoctorSerializer(data=request.data, context={'user': request.user, 'special': speciality})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        obj = get_object_or_404(Doctors, details=request.user)

        # Check if 'specialized_in_id' is provided and retrieve the Specialities object
        context = {}
        specialized_in_id = request.data.get('specialized_in')
        if specialized_in_id:
            context = {'special': get_object_or_404(Specialities, id=specialized_in_id)}

        # Update the existing doctor profile for the user
        serializer = self.serializer_class(instance=obj, data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class FilterAppointmentView(APIView):
    permission_classes = [IsAuthenticated, IsDoctor]

    def get(self, request, *args, **kwargs):
        now = datetime.now()

        # Get the filtering parameter from the request (completed, active, upcoming)
        status = request.query_params.get('status', None)

        # Set up the query for filtering
        if status == 'completed':
            query = Q(date_time_end__lt=now)
        elif status == 'active':
            query = Q(date_time_start__lte=now, date_time_end__gt=now)
        elif status == 'upcoming':
            query = Q(date_time_start__gt=now)
        else:
            return Response({'error': 'Invalid status parameter'}, status=406)

        doctor = get_object_or_404(Doctors, details=request.user.id)
        appointments = Appointments.objects.filter(doctor=doctor.id).filter(query)
        serializer = AppointmentSerializer(appointments, many=True)
        return Response(data=serializer.data)
