from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Faculty
from .serializers import FacultyListSerializer, FacultyDetailSerializer


class FacultyListAPIView(ListAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultyListSerializer


class FacultyDetailAPIView(RetrieveAPIView):
    queryset = Faculty.objects.all()
    serializer_class = FacultyDetailSerializer
