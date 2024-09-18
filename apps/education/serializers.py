from rest_framework import serializers
from apps.education.models import Faculty, Director, Direction


class FacultyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = ("id", "title", "degree")


class DirectorModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = ("full_name", "bio", "phone_number", "picture")


class DirectionModelSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField()
    education_type = serializers.SerializerMethodField()

    class Meta:
        model = Direction
        fields = ("title", "language", "body", "education_type")

    def get_language(self, obj):
        return obj.get_language_display()

    def get_education_type(self, obj):
        return obj.get_education_type_display()


class FacultyDetailSerializer(serializers.ModelSerializer):
    director = DirectorModelSerializer()
    directions = DirectionModelSerializer(many=True)
    degree = serializers.SerializerMethodField()
    yangi_field = serializers.SerializerMethodField()

    class Meta:
        model = Faculty
        fields = ("title", "body", "degree", "director", "directions", "yangi_field")

    def get_degree(self, obj):
        return obj.get_degree_display()

    def get_yangi_field(self, obj):
        return "Yangi field"
