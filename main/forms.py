from django import forms

from .models import Complain


class ComplainForm(forms.ModelForm):
    """Form for validating Complain."""
    complain_image = forms.ImageField(required=False)
    class Meta:
        model = Complain
        fields = ['complain_title', 'complain_message', 'complain_image', 'to_complain']