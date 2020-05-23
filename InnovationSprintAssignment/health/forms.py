# forms file
from django import forms
from django.contrib.auth.models import User
from health.models import UserTemps
from django.contrib.admin import widgets

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ('username', 'email', 'password')
class UserProfileForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'email',)
class TempsForm(forms.ModelForm):
	temperature = forms.FloatField(help_text = 'Please Input Temperature')
	timeStamp = forms.DateTimeField()
	# user = forms.ModelChoiceField(queryset=User.objects.none(), widget=forms.HiddenInput)
	class Meta:
		model = UserTemps
		exclude=('user',)
		fields = ('temperature','timeStamp',)
