# forms file
from django import forms
from django.contrib.auth.models import User
from health.models import UserTemps,UserFeverSessions
from django.contrib.admin import widgets
import datetime
def default_start_time():
    now = datetime.datetime.now
    start = now.replace(hour=22, minute=0, second=0, microsecond=0)
    return start if start > now else start + timedelta(days=1) 

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ('username', 'email', 'password')
class UserProfileForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'email',)
class SelectedSessionsForm(forms.Form):
	startTime = forms.DateTimeField()
	endTime = forms.DateTimeField()
	# def __init__(self, *args, **kwargs):
	# 	self._user = kwargs.pop('user')
	# 	super(SelectedSessionsForm, self).__init__(*args, **kwargs)
	# def get_results(self):
	# def save(self, commit=True):
	# 	inst = super(SelectedSessionsForm, self).save(commit=False)
	# 	inst.user = self._user
	# 	if commit:
	# 		inst.save()
	# 		self.save_m2m()
	# 	return inst
	# class Meta:
	# 	model = UserFeverSessions
	# 	exclude=('user',)
	# 	fields = ('startTime','endTime',)

class TempsForm(forms.ModelForm):
	temperature = forms.FloatField(help_text = 'Please Input Temperature')
	# timeStamp = forms.DateTimeField(default=default_start_time())
	# user = forms.ModelChoiceField(queryset=User.objects.none(), widget=forms.HiddenInput)
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