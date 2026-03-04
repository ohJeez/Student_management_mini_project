from django.test import TestCase
from django.urls import reverse
from .models import Student


class SimpleTest(TestCase):
    def setUp(self):
        # create test user and login
        from django.contrib.auth.models import User
        self.user = User.objects.create_user('tester', 'tester@example.com', 'pass')
        self.client.login(username='tester', password='pass')
        self.student = Student.objects.create(
            first_name='John',
            last_name='Doe',
            email='john@example.com',
            roll_number='R123'
        )

    def test_list(self):
        response = self.client.get(reverse('student-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John')

    def test_create(self):
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane@example.com',
            'roll_number': 'R124',
            'enrollment_date': '2026-01-01',
        }
        response = self.client.post(reverse('student-create'), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Student.objects.filter(email='jane@example.com').exists())

    def test_update(self):
        url = reverse('student-update', args=[self.student.pk])
        data = {
            'first_name': 'Johnny',
            'last_name': 'Doe',
            'email': 'john@example.com',
            'roll_number': 'R123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.student.refresh_from_db()
        self.assertEqual(self.student.first_name, 'Johnny')

    def test_delete(self):
        url = reverse('student-delete', args=[self.student.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Student.objects.filter(pk=self.student.pk).exists())

    def test_detail(self):
        url = reverse('student-detail', args=[self.student.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'John')

    def test_login_required(self):
        # logout client to check redirect
        self.client.logout()
        resp = self.client.get(reverse('student-list'))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/accounts/login/'))

    def test_login_logout_flow(self):
        # already logged in by setUp
        resp = self.client.get(reverse('student-list'))
        self.assertEqual(resp.status_code, 200)
        # logout via view and also clear client
        logout_resp = self.client.post(reverse('logout'))
        self.assertEqual(logout_resp.status_code, 302)
        self.client.logout()
        resp2 = self.client.get(reverse('student-list'))
        self.assertEqual(resp2.status_code, 302)
