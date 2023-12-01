from django.urls import path

from .views import DoctorsListView, DoctorView, AvailableTimeView

urlpatterns = [
    path('doctors/<int:sp_id>/', DoctorsListView.as_view()),
    path('doctor/<int:doc_id>/', DoctorView.as_view()),
    path('times/<int:doc_id>/<str:a_date>/', AvailableTimeView.as_view()),

    # path('times/<int:doc_id>/', AvailableDateView.as_view()),
]

# (GET) patient/doctors/7/ => get doctors by specialities
# (GET) patient/doctor/7/ => get doctor
# (GET) patient/times/7/2022-08-11/ => get available date time1
