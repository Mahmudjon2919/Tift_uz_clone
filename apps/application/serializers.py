from rest_framework import serializers
from .models import Application
from rest_framework.exceptions import ValidationError
from apps.education.serializers import DirectionModelSerializer
from apps.common.serializer import DistrictsSerializer


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("first_name",
                  "last_name",
                  "passport",
                  "pinfl", "gender",
                  "direction",
                  "district",
                  "birth_date")

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        if Application.objects.filter(passport=validated_data['passport']).exists():  # Corrected line
            raise ValidationError({
                "passport": "Application already created with this passport data"
            })
        return super().create(validated_data)


class ApplicationDetailSerializer(serializers.ModelSerializer):
    direction = DistrictsSerializer()
    district = DistrictsSerializer()

    status = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ("first_name",
                  "last_name",
                  "passport",
                  "pinfl", "gender",
                  "direction",
                  "district",
                  "birth_date", "gender", "status", "accepted_at", "created")
    def get_status(self, obj):
        return obj.get_status_display()

    def get_gender(self, obj):
        return obj.get_gender_display()
