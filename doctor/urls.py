from django.urls import path

from doctor.views import SpecialitiesView, DoctorDetailsView

urlpatterns = [
    path('specialities/', SpecialitiesView.as_view()),
    path('doctor/', DoctorDetailsView.as_view()),
]

# (GET) doctor/specialities/ => get all specialities
# (GET) doctor/doctor/ => get doctors details
# (POST) doctor/doctor/ => create doctors details
# (PUT) doctor/doctor/ => update doctors details
