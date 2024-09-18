from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from apps.education.models import Faculty, Director, Direction


class FacultyAPITestCase(TestCase):
    def setUp(self):
        # Create a Director instance
        self.director = Director.objects.create(
            full_name="John Doe",
            bio="An experienced academic",
            phone_number="123456789",
            picture="director_picture.png"
        )

        # Create a Faculty instance
        self.faculty = Faculty.objects.create(
            title="Computer Science",
            body="Faculty of Computer Science",
            degree="BSc",
            director=self.director
        )

        # Create a Direction instance related to the Faculty
        self.direction = Direction.objects.create(
            title="Software Engineering",
            body="Focuses on software development",
            faculty=self.faculty,
            language="English",
            education_type="Full-time"
        )

        self.client = APIClient()

    def test_faculty_list(self):
        response = self.client.get('/api/v1/faculties/')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['title'], "Computer Science")

    def test_faculty_detail(self):
        response = self.client.get(f'/api/v1/faculties/{self.faculty.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], "Computer Science")
        self.assertEqual(response.data['director']['full_name'], "John Doe")
        self.assertEqual(response.data['directions'][0]['title'], "Software Engineering")