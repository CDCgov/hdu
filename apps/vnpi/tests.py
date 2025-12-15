from django.test import TestCase
from django.urls import reverse

__author__ = 'Alan Viars'

class VerifyNPIAPITestCase(TestCase):
    def test_verify_npi_happy_path(self):
        """Test successful NPI verification with valid NPI number"""
        npi_number = "1144203563"
        url = reverse('vnpi:api', args=[npi_number])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertIn('number', json_response)
        self.assertEqual(json_response['valid'], True)

    def test_verify_npi_invalid_number(self):
        """Test NPI verification with invalid but numeric NPI number"""
        npi_number = "1144203564"
        url = reverse('vnpi:api', args=[npi_number])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.json())
        json_response = response.json()
        self.assertIn('number', json_response)
        self.assertEqual(json_response['valid'], False)


    def test_verify_npi_non_numeric(self):
        """Test NPI verification with non-numeric input"""
        npi_number = "foobar"
        url = reverse('vnpi:api', args=[npi_number])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('error', response.json())
        json_response = response.json()
        self.assertIn('number', json_response)
        self.assertEqual(json_response['valid'], False)


