from rest_framework import serializers
from apps.news.models import NewsContent


class NewsContentSerializer(serializers.ModelSerializer):
    class Meta:
        model=NewsContent
        fields=("title",  "slug", "publish_time", )


class NewsContentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=NewsContent
        fields = ("title", "body", "slug", "publish_time",)