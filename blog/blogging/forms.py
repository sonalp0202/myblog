from django.contrib.auth.forms import UserCreationForm,UserChangeForm,ReadOnlyPasswordHashField
from .models import CustomUser
from django import forms

class RegisterUser(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name']

    def clean_email(self):
        email = self.cleaned_data['email']
        users = CustomUser.objects.filter(email__iexact=email)
        if users:
            raise forms.ValidationError("Custom text about email.")
        return email.lower()


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUserChange(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ['email']