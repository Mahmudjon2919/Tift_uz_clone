from django.urls import path
from .views import FacultyListAPIView, FacultyDetailAPIView

urlpatterns=[
    path("faculties/", FacultyListAPIView.as_view()),
    path("faculties/<int:pk>/", FacultyDetailAPIView.as_view())
]