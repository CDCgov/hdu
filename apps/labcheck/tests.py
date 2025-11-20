from django.test import TestCase, Client
from django.urls import reverse
from pathlib import Path
import json
class LabCheckViewsTest(TestCase):
	def setUp(self):
		self.client = Client()
		self.adt_path = Path(__file__).parent / 'test_files' / 'adt.hl7'
		self.bad_hl7_path = Path(__file__).parent / 'test_files' / 'bad-hl7.hl7'
		self.good_hl7_path = Path(__file__).parent / 'test_files' / 'redacted-lab-message.hl7'

	def test_index_view_good_hl7(self):
		with open(self.adt_path, 'r', encoding='utf-8') as f:
			hl7_content = f.read()
		response = self.client.post(reverse('labcheck:index'), {'hl7-input': hl7_content})
		self.assertEqual(response.status_code, 200)
		#self.assertContains(response, 'FHIR Output')
		# Check that FHIR Bundle is present in context
		#self.assertIn('fhir_output', response.context)
		#json_dict = json.loads(response.context['fhir_output'])
		#self.assertIsInstance(json_dict, dict)
		#self.assertIn('resourceType', json_dict)
		#self.assertEqual(json_dict['resourceType'], 'Bundle')

	def test_api_index_good_hl7(self):
		with open(self.good_hl7_path, 'rb') as f:
			response = self.client.post(reverse('labcheck:api_index'), {'hl7_file': f})
		self.assertEqual(response.status_code, 200)
		# data = response.json()
		#self.assertIn('resourceType', data)
		#self.assertEqual(data['resourceType'], 'Bundle')


