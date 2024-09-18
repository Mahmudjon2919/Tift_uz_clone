from apps.news.serializers import NewsContentSerializer, NewsContentDetailSerializer
from apps.news.models import NewsContent
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.utils import timezone

class NewsContentListAPIView(ListAPIView):
    queryset = NewsContent.objects.filter(
        is_published=True,
        publish_time__lte=timezone.now()
    ).order_by("-id")
    serializer_class = NewsContentSerializer


class NewsContentDetailAPIView(RetrieveAPIView):
    queryset = NewsContent.objects.filter(
        is_published=True,
        publish_time__gte=timezone.now()
    ).order_by("-id")
    serializer_class = NewsContentSerializer
    lookup_field = "slug"
