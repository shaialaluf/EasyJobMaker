
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import *
from .models import *
from django import forms


class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		#full_name = forms.CharField(max_length=200)
		fields = ['first_name','last_name', 'username', 'email', 'password1', 'password2']
