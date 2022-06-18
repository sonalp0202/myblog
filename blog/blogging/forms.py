from django.contrib.auth.forms import UserCreationForm,UserChangeForm,ReadOnlyPasswordHashField
from .models import CustomUser
from django import forms

class RegisterUser(UserCreationForm):
    mobile = forms.CharField()
    class Meta:
        model = CustomUser
        fields = ['email','first_name','last_name','mobile']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

class CustomUserChange(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ['email']