from django.contrib import admin
from  apps.common import models

# Register your models here.
@admin.register(models.Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "order_id")
    list_editable = ("order_id",)

@admin.register(models.District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "region__title", "order_id")
    list_editable = ("order_id",)
@admin.register(models.Social)
class SocialAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "social", "link")
    list_editable = ("title", "social", "link")