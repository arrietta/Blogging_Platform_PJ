from django.contrib.auth.forms import UserCreationForm
from .models import Post
from django import forms
from django.contrib.auth.models import User
from .models import Profile

class ProfileRegistrationForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'surname', 'info', 'image']

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username',  'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

