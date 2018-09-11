from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
	first_name = forms.CharField(max_length=50, required=True, help_text='Required.', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}))
	last_name = forms.CharField(max_length=50, required=True, help_text='Required.', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}))
	email = forms.EmailField(max_length=254, help_text = 'Required. Supply a valid email', widget=forms.TextInput(attrs={'class': 'form-control', 'aria-describedby':'emailHelp', 'placeholder': 'Enter Email'}))
	password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Create Password'}))
	password2 = forms.CharField(label="Confirm Password", widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
	
	class Meta:
		model = User
		fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
		widgets = {
			'username': forms.TextInput(attrs = {'class': 'form-control', 'placeholder':'Create Username'})
		}
		