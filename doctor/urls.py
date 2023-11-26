from django.urls import path

from doctor.views import SpecialitiesView, DoctorDetailsView

urlpatterns = [
    path('specialities/', SpecialitiesView.as_view()),
    path('doctor/', DoctorDetailsView.as_view()),
]
