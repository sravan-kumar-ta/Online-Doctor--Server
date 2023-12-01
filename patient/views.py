from datetime import datetime, timedelta

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from doctor.models import Doctors
from patient.models import Appointments
from patient.serializers import DoctorSerializer, AvailableTimeSerializer


class DoctorsListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = DoctorSerializer

    def get_queryset(self):
        sp_id = self.kwargs['sp_id']
        return Doctors.objects.filter(specialized_in=sp_id)


class DoctorView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DoctorSerializer

    def get(self, request, *args, **kwargs):
        doctor = get_object_or_404(Doctors, id=kwargs['doc_id'])
        serializer = self.serializer_class(doctor)
        return Response(serializer.data)


# class AvailableDateView(RetrieveAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = AvailableTimeSerializer
#
#     def get(self, request, *args, **kwargs):
#         doctor = get_object_or_404(Doctors, id=kwargs['doc_id'])
#         serializer = self.serializer_class(doctor)
#         return Response(serializer.data)


def getStartEndTime(doctor, day, modified_date):
    time_start = None
    time_end = None
    if day == 1:
        time_start = doctor.mon_start
        time_end = doctor.mon_end
    elif day == 2:
        time_start = doctor.tue_start
        time_end = doctor.tue_end
    elif day == 3:
        time_start = doctor.wed_start
        time_end = doctor.wed_end
    elif day == 4:
        time_start = doctor.thu_start
        time_end = doctor.thu_end
    elif day == 5:
        time_start = doctor.fri_start
        time_end = doctor.fri_end
    elif day == 6:
        time_start = doctor.sat_start
        time_end = doctor.sat_end
    elif day == 7:
        time_start = doctor.sun_start
        time_end = doctor.sun_end
    try:
        return datetime.combine(modified_date, time_start), datetime.combine(modified_date, time_end)
    except:
        return None, None


class AvailableTimeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AvailableTimeSerializer

    def get(self, request, *args, **kwargs):
        doctor_id = kwargs.get('doc_id')
        date = kwargs['a_date']

        modified_date = datetime.strptime(date, "%Y-%m-%d").date()
        day = modified_date.isoweekday()
        duration = timedelta(minutes=30)

        # Appointments are taken according to the requested date and time
        appointments = Appointments.objects.filter(Q(doctor_id=doctor_id) & Q(date=modified_date))

        doctor = Doctors.objects.get(pk=doctor_id)

        # take starting and ending time of day of the requested doctor
        start_time, end_time = getStartEndTime(doctor, day, modified_date)

        booked_slots = set()
        for appointment in appointments:
            booked_slots.add(
                datetime.combine(modified_date, appointment.time)
            )

        available_slots = {}
        if start_time:
            count = 0
            while True:
                if start_time not in booked_slots:
                    start = datetime.strftime(start_time, "%I:%M %p")
                    add_30 = start_time + timedelta(minutes=30)
                    end = datetime.strftime(add_30, "%I:%M %p")
                    available_slots[count] = {'start': start, 'end': end}
                    count += 1
                start_time += duration
                if start_time + duration > end_time:
                    break

        return Response({'slots': available_slots}, status=status.HTTP_200_OK)
