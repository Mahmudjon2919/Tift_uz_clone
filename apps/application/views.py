from rest_framework.generics import CreateAPIView, ListAPIView
from .serializers import ApplicationCreateSerializer, ApplicationDetailSerializer
from .models import Application
from rest_framework.permissions import IsAuthenticated
from django.views.generic import TemplateView

class ApplicationCreateAPIView(CreateAPIView):
    serializer_class = ApplicationCreateSerializer
    queryset = Application
    permission_classes = (IsAuthenticated,)


class ApplicationStatusesListAPIView(ListAPIView):
    serializer_class = ApplicationDetailSerializer
    queryset = Application.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)

class StudentApplicationTemplateview(TemplateView):
    template_name = "application.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        application_id = self.request.GET.get("application_id")

        try:
            if application_id:
                context['application'] = Application.objects.get(id=application_id)
        except Application.DoesNotExist:
            context['application'] = None
            context['error_message'] = "Application not found"

        return context