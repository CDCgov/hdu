from django.test import TestCase, Client
from django.urls import reverse
from pathlib import Path
import json
class CDA2FHIRViewsTest(TestCase):
	def setUp(self):
		self.client = Client()
		self.good_ccda_path = Path(__file__).parent / 'test_files' / 'good-ccda.xml'
		self.bad_ccd_path = Path(__file__).parent / 'test_files' / 'bad-ccda.xml'

	def test_index_view_good_ccda(self):
		with open(self.good_ccda_path, 'r', encoding='utf-8') as f:
			ccda_content = f.read()
		response = self.client.post(reverse('cda2fhir:index'), {'cda-input': ccda_content})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'FHIR Output')
		# Check that FHIR Bundle is present in context
		self.assertIn('fhir_output', response.context)
		json_dict = json.loads(response.context['fhir_output'])
		self.assertIsInstance(json_dict, dict)
		self.assertIn('resourceType', json_dict)
		self.assertEqual(json_dict['resourceType'], 'Bundle')

	def test_index_view_bad_ccd(self):
		with open(self.bad_ccd_path, 'r', encoding='utf-8') as f:
			ccda_content = f.read()
		response = self.client.post(reverse('cda2fhir:index'), {'cda-input': ccda_content})
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, 'FHIR Output')
		self.assertIn('fhir_output', response.context)
		self.assertIsInstance(response.context['fhir_output'], dict)
		self.assertIn('error', response.context['fhir_output'])

	def test_api_index_good_ccda(self):
		with open(self.good_ccda_path, 'rb') as f:
			response = self.client.post(reverse('cda2fhir:api_index'), {'cda_file': f})
		self.assertEqual(response.status_code, 200)
		data = response.json()
		self.assertIn('resourceType', data)
		self.assertEqual(data['resourceType'], 'Bundle')

	def test_api_index_bad_ccd(self):
		with open(self.bad_ccd_path, 'rb') as f:
			response = self.client.post(reverse('cda2fhir:api_index'), {'cda_file': f})
		self.assertEqual(response.status_code, 500)
		data = response.json()
		self.assertIn('error', data)
