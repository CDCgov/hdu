from django import forms
from gdc.get_direct_certificate import DCert

class DirectCheckForm(forms.Form):
    endpoint = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Paste Direct endpoint here'}),
        label='Direct Endpoint',
        required=True
    )
    def clean_endpoint(self):
        endpoint = self.cleaned_data.get('endpoint', "").strip().lower()
        endpoint = endpoint.replace("@", ".")
        # print("Cleaned endpoint:", endpoint)  # Debug statement
        dc = DCert(endpoint)
        dc.validate_certificate(False)
        # print("DCert result:", dc.result)  # Debug statement
        if dc.result.get('is_found', False) is False:
            raise forms.ValidationError("The Direct endpoint not found or invalid.")

        return endpoint
