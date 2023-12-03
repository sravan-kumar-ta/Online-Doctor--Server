from datetime import datetime, timedelta

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor.models import Doctors
from patient import serializers
from patient.models import Appointments
from patient.permissions import IsPatient


class DoctorsListView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.DoctorSerializer

    def get_queryset(self):
        sp_id = self.kwargs['sp_id']
        return Doctors.objects.filter(specialized_in=sp_id)


class DoctorView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.DoctorSerializer

    def get(self, request, *args, **kwargs):
        doctor = get_object_or_404(Doctors, id=kwargs['doc_id'])
        serializer = self.serializer_class(doctor)
        return Response(serializer.data)


def getStartEndTime(doctor, day, modified_date):
    days_mapping = {
        1: ('mon_start', 'mon_end'),
        2: ('tue_start', 'tue_end'),
        3: ('wed_start', 'wed_end'),
        4: ('thu_start', 'thu_end'),
        5: ('fri_start', 'fri_end'),
        6: ('sat_start', 'sat_end'),
        7: ('sun_start', 'sun_end'),
    }

    time_start_attr, time_end_attr = days_mapping.get(day, (None, None))

    if time_start_attr is not None and time_end_attr is not None:
        time_start = getattr(doctor, time_start_attr)
        time_end = getattr(doctor, time_end_attr)

        try:
            return datetime.combine(modified_date, time_start), datetime.combine(modified_date, time_end)
        except:
            pass

    return None, None


class AvailableTimeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AvailableTimeSerializer

    def get(self, request, *args, **kwargs):
        doctor_id = kwargs.get('doc_id')
        date = kwargs['a_date']

        modified_date = datetime.strptime(date, "%Y-%m-%d").date()
        day = modified_date.isoweekday()
        duration = timedelta(minutes=30)

        doctor = get_object_or_404(Doctors, pk=doctor_id)

        # take starting and ending time of day of the requested doctor
        start_time, end_time = getStartEndTime(doctor, day, modified_date)

        # Appointments are taken according to the requested date and time
        appointments = Appointments.objects.filter(Q(doctor_id=doctor_id) & Q(date=modified_date))
        booked_slots = {datetime.combine(modified_date, appointment.time) for appointment in appointments}

        available_slots = []
        if start_time:
            while start_time + duration <= end_time:
                if start_time not in booked_slots:
                    start = datetime.strftime(start_time, "%I:%M %p")
                    end = datetime.strftime(start_time + duration, "%I:%M %p")
                    available_slots.append({'start': start, 'end': end})
                start_time += duration

        return Response({'slots': available_slots}, status=status.HTTP_200_OK)


class CreateAppointmentView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, IsPatient)
    queryset = Appointments.objects.all()
    serializer_class = serializers.AppointmentSerializer


class FilterAppointmentView(APIView):
    permission_classes = [IsAuthenticated, IsPatient]
    serializer_class = serializers.AvailableTimeSerializer

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

        appointments = Appointments.objects.filter(query)
        serializer = serializers.AppointmentSerializer(appointments, many=True)
        return Response(data=serializer.data)
