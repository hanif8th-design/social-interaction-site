from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from accounts.models import Profile


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=150,
    widget=forms.TextInput(attrs={'placeholder':'Enter username here','class':'form-control'})
    )

    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter password here','class':'form-control'}))

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','password1','password2']




class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email','first_name','last_name']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture','bio','location','website']






