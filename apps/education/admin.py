from django.contrib import admin
from apps.education import models


@admin.register(models.Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone_number", )

@admin.register(models.Direction)
class DiretionAdmin(admin.ModelAdmin):
    list_display = ("title", "faculty", )

@admin.register(models.Faculty)
class FacultyAdmin(admin.ModelAdmin):

    list_display = ("title", "degree", "director", )