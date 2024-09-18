from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth.models import User
from apps.application.models import Application, ApplicationStatusChoices, Gender
from apps.common.models import District, Region # Assuming District model exists
from apps.education.models import Direction, Faculty



class ApplicationAPITestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.login(username='testuser', password='testpass')

        self.faculty = Faculty.objects.create(title="Engineering")
        self.direction = Direction.objects.create(title="Matematika", faculty=self.faculty)
        self.region = Region.objects.create(title="Test Region", order_id=1)
        self.district = District.objects.create(title="Shovot", region=self.region, order_id=1)
        self.application_data = {
            "first_name": "John",
            "last_name": "Doe",
            "passport": "AB1234567",
            "pinfl": "12345678901234",
            "gender": Gender.MALE,
            "birth_date": "1990-01-01",
            "direction": self.direction.id,
            "district": self.district.id,
        }

    def test_application_create(self):
        url = reverse('application-create')
        response = self.client.post(url, self.application_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Application.objects.count(), 1)
        application = Application.objects.first()
        self.assertEqual(application.first_name, "John")
        self.assertEqual(application.last_name, "Doe")

    def test_application_create_duplicate_passport(self):
        Application.objects.create(user=self.user, **self.application_data)
        url = reverse('application-create')
        response = self.client.post(url, self.application_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("passport", response.data)

    def test_application_status_list(self):
        application = Application.objects.create(
            user=self.user,
            **self.application_data,
            status=ApplicationStatusChoices.PENDING
        )
        url = reverse('application-status')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['first_name'], "John")
        self.assertEqual(response.data[0]['last_name'], "Doe")
        self.assertEqual(response.data[0]['status'], application.get_status_display())

    def test_application_status_list_no_applications(self):
        url = reverse('application-status')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_application_create_invalid_data(self):
        # Missing required field
        invalid_data = {**self.application_data}
        del invalid_data['first_name']
        url = reverse('application-create')
        response = self.client.post(url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('first_name', response.data)

    def test_application_create_unauthenticated(self):
        self.client.logout()
        url = reverse('application-create')
        response = self.client.post(url, self.application_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)