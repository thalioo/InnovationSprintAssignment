# forms file
from django import forms
from django.contrib.auth.models import User
from health.models import UserTemps,UserFeverSessions
from django.contrib.admin import widgets
import datetime
'''

'''
class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ('username', 'email', 'password')
class UserProfileForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'email','first_name','last_name')
class SelectedSessionsForm(forms.Form):
	startTime = forms.DateTimeField()
	endTime = forms.DateTimeField()

class TempsForm(forms.ModelForm):
	temperature = forms.FloatField(help_text = 'Please Input Temperature')
	def __init__(self, *args, **kwargs):
		self._user = kwargs.pop('user')
		super(TempsForm, self).__init__(*args, **kwargs)

	def save(self, commit=True):
		inst = super(TempsForm, self).save(commit=False)
		inst.user = self._user
		if commit:
			inst.save()
			self.save_m2m()
		return inst
	class Meta:
		model = UserTemps
		exclude=('user','active')
		fields = ('temperature',)