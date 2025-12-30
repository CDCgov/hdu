from django import forms
from .fhirec import check_if_url_is_valid

class FHIRInspectorForm(forms.Form):
    url = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Paste FHIR server URL'}),
        label='FHIR URL',
        required=True
    )
    include_details = forms.BooleanField(
        label='Include Detailed Analysis',
        required=False,
        initial=False
    )
    def clean_url(self):
        url = self.cleaned_data.get('url', "").strip()
        if check_if_url_is_valid(url)is False:
            raise forms.ValidationError("The URL appears to be invalid or malformed.")
        return url
