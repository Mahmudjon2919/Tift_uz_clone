from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.common.models import Region, District, Social

class CommonAPITests(APITestCase):

    def setUp(self):
        self.region = Region.objects.create(title="Test Region", order_id=1)
        self.district = District.objects.create(title="Test District", region=self.region, order_id=1)
        self.social = Social.objects.create(title="Test Social", social=Social.SocialMediaChoices.TELEGRAM, link="https://t.me/test")

    def test_region_list(self):
        url = reverse('region-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data['results'][0]['title'], self.region.title)

    def test_district_list_by_region(self):
        url = reverse('district-list-by-region', args=[self.region.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data['results'][0]['title'], self.district.title)

    def test_social_list(self):
        url = reverse('social-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
        self.assertEqual(response.data['results'][0]['title'], self.social.title)

    def test_gender_choices(self):
        url = reverse('gender-choices')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['key'], 'male')
        self.assertEqual(response.data[1]['key'], 'female')