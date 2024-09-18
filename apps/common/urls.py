from django.urls import path
from apps.common.views import RegionListAPIView, DistrictListByRegionAPIView, SocialListAPIView, GenderChoicesAPIView

urlpatterns = [
    path('regions/', RegionListAPIView.as_view(), name="region-list" ),
    path('<int:pk>/districts/', DistrictListByRegionAPIView.as_view(), name="district-list-by-region"),
    path('socials/', SocialListAPIView.as_view(), name="social-list"),
    path('genders/', GenderChoicesAPIView.as_view(), name="gender-choices")
]

