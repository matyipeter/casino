from .models import UserProfile
from django.contrib.auth.models import User
from django import forms


class UserCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserProfileForm(forms.ModelForm):
    class Meta():
        model = UserProfile
        fields = ['birth_date']



