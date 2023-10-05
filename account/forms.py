from django import forms


class SignupForm(forms.Form):
    """Form for  validating user creation."""
    first_name = forms.CharField()
    last_name = forms.CharField()
    username = forms.CharField()
    email = forms.EmailField()
    phone_number = forms.IntegerField()
    password = forms.CharField()
    retype_password = forms.CharField()