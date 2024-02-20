from django import forms

from .models import Complain


class ComplainForm(forms.ModelForm):
    """Form for validating Complain."""
    complain_image = forms.ImageField(required=False)
    class Meta:
        model = Complain
        fields = ['complain_title', 'complain_message', 'complain_image', 'to_complain']


class ComplainSearch(forms.ModelForm):
    search_title=forms.CharField(required=False)
    from_date=forms.DateTimeField(required=False)
    to_date=forms.DateTimeField(required=False)

class UserSearch(forms.ModelForm):
    Search_titile=forms.CharField(required='False')
