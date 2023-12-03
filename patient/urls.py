from django.urls import path

from . import views

urlpatterns = [
    path('doctors/<int:sp_id>/', views.DoctorsListView.as_view()),
    path('doctor/<int:doc_id>/', views.DoctorView.as_view()),
    path('times/<int:doc_id>/<str:a_date>/', views.AvailableTimeView.as_view()),
    path('create-appointment/', views.CreateAppointmentView.as_view()),
    path('filter-appointment/', views.FilterAppointmentView.as_view()),
]

# (GET) patient/doctors/7/ => get doctors by specialities
# (GET) patient/doctor/7/ => get doctor
# (GET) patient/times/7/2022-08-11/ => get available times
# (POST) patient/create-appointment/ => create an appointment
# (GET) patient/filter-appointment/ => get filtered appointments
