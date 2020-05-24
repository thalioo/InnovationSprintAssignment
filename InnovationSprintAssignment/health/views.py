from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
# from rest_framework_swagger.views import get_swagger_view
from django.http import HttpResponseRedirect, HttpResponse,JsonResponse
from django.urls  import reverse
from health.forms import UserForm,TempsForm,UserProfileForm,SelectedSessionsForm
from django.shortcuts import render,get_object_or_404
from health.models import UserTemps,UserFeverSessions
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView,FormView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View

@login_required
def profile(request):
	try:
		user = User.objects.get(username=request.user)
		print('found')
	except User.DoesNotExist:
		return redirect('index')
	userprofile = User.objects.get(id=user.id)
	form = UserProfileForm()
	return render(request, 'health/profile.html',
	{'userprofile': userprofile, 'form': form})

@login_required
def index(request):
    return HttpResponse("Hello, you are at the HealthApp HomePage")
@login_required
def success(request):
	return HttpResponse("Succesully added a Temperature!")
def register(request):
# A boolean value for telling the template
# whether the registration was successful.
# Set to False initially. Code changes value to
# True when registration succeeds.
	registered = False
	# If it's a HTTP POST, we're interested in processing form data.
	if request.method == 'POST':
	# Attempt to grab information from the raw form information.
	# Note that we make use of both UserForm and UserProfileForm.
		user_form = UserForm(data=request.POST)
		# If the two forms are valid...
		if user_form.is_valid():
		# Save the user's form data to the database.
			user = user_form.save()
			# Now we hash the password with the set_password method.
			# Once hashed, we can update the user object.
			user.set_password(user.password)
			user.save()

			# Update our variable to indicate that the template
			# registration was successful.
			registered = True
		else:
		# Invalid form or forms - mistakes or something else?
		# Print problems to the terminal.
			print(user_form.errors)
	else:
		# Not a HTTP POST, so we render our form using two ModelForm instances.
		# These forms will be blank, ready for user input.
		user_form = UserForm()
		# Render the template depending on the context.
	return render(request,
	'health/register.html',
	{'user_form': user_form,
	'registered': registered})
		# Now sort out the UserProfile instance.
		# Since we need to set the user attribute ourselves,
		# we set commit=False. This delays saving the model
		# until we're ready to avoid integrity problems.

def user_login(request):
# If the request is a HTTP POST, try to pull out the relevant information.
	if request.method == 'POST':
		# Gather the username and password provided by the user.
		# This information is obtained from the login form.
		# We use request.POST.get('<variable>') as opposed
		# to request.POST['<variable>'], because the
		# request.POST.get('<variable>') returns None if the
		# value does not exist, while request.POST['<variable>']
		# will raise a KeyError exception.
		username = request.POST.get('username')
		password = request.POST.get('password')
		# Use Django's machinery to attempt to see if the username/password
		# combination is valid - a User object is returned if it is.
		user = authenticate(username=username, password=password)
		# If we have a User object, the details are correct.
		# If None (Python's way of representing the absence of a value), no user
		# with matching credentials was found.
		if user:
			# Is the account active? It could have been disabled.
			if user.is_active:
			# If the account is valid and active, we can log the user in.
			# We'll send the user back to the homepage.
				login(request, user)
				return HttpResponseRedirect(reverse('index'))
			else:
			# An inactive account was used - no logging in!
				return HttpResponse("Your Health account is disabled.")
		else:
		# Bad login details were provided. So we can't log the user in.
			print("Invalid login details: {0}, {1}".format(username, password))
			return HttpResponse("Invalid login details supplied.")
		# The request is not a HTTP POST, so display the login form.
		# This scenario would most likely be a HTTP GET.
	else:
	# No context variables to pass to the template system, hence the
	# blank dictionary object...
		return render(request, 'health/login.html', {})


def manipulateFeverSessions(form):
	temperature = form.temperature
	model = UserFeverSessions()
	try:
		user_sesions = UserFeverSessions.objects.filter(pk=form.user.id)
		user_sesions = UserFeverSessions.objects.get(active_session=True)
		print('found')
	except UserFeverSessions.DoesNotExist:
		user_sesions = None
	#if user has no fever sessions and needs to create one 
	if not user_sesions and temperature >=37:
		model.user=form.user
		model.startTime = form.timeStamp
		model.active_session = True
		model.endTime =None
		model.save()
	else :
		#if user has an active fever session and needs to close it
		if user_sesions and temperature < 37:
			model.startTime = user_sesions.startTime
			model.endTime = form.timeStamp
			model.user=form.user
			model.active_session = False
			model.pk = user_sesions.pk
			model.save()
def makeTempsInactive(form):
	try:
		user_temps = UserTemps.objects.filter(user=form.user)
		print(user_temps)
		user_temps = UserTemps.objects.filter(active=True).update(active=False)
	except UserFeverSessions.DoesNotExist:
		user_sesions = None

class AddTempCreateView(LoginRequiredMixin,CreateView):
	template_name = 'health/add_temperature.html'
	form_class = TempsForm
	def form_valid(self, form):
		self.object = form.save(commit=False)
		self.object.user = self.request.user
		self.object.active = True
		manipulateFeverSessions(self.object)
		makeTempsInactive(self.object)
		self.object.save()
		return success(self.request)

	def get_form_kwargs(self, *args, **kwargs):
		kwargs = super(AddTempCreateView, self).get_form_kwargs(*args, **kwargs)
		kwargs['user'] = self.request.user
		return kwargs


class SessionView(LoginRequiredMixin,FormView):
	template_name = 'health/view_sessions_dates.html'
	form_class = SelectedSessionsForm
	success_url = '/index/'
	def form_valid(self, form):
		# form =SelectedSessionsForm(self.request.body)
		sessions = UserFeverSessions.objects.filter(user = self.request.user,startTime__range=[form.cleaned_data['startTime'],form.cleaned_data['endTime']],
			endTime__range=[form.cleaned_data['startTime'],form.cleaned_data['endTime']])
		# session_temps = UserTemps.objects.filter()
		session_temperatures = []
		res = {}
		i=0
		for x in sessions:
			res[i] = {}
			res[i]['id']=x.id
			res[i]['temps']={}
			res[i]['startTime']=x.startTime
			res[i]['endTime']=x.endTime
			q = UserTemps.objects.filter(user=self.request.user,timeStamp__gte=x.startTime,timeStamp__lt=x.endTime)
			for t in q:
				res[i]['temps'][x.timeStamp]=(t.temperature)
			i+=1
		# res[self.user.user.id] = 
		# res = []
		# for y in session_temperatures:
		# 	res.append(y.temperature)
		# print(session_temperatures)
		# print('-----')
		# print(res)
		# print('-----')

		# except: return index(self.request)
		return JsonResponse(res)


class TemperatureView(LoginRequiredMixin,ListView):
	template_name = 'health/temp-list.html'
	# queryset = UserTemps.objects.get(pk=request.user.id)
	context_object_name = 'temps'
	def get_queryset(self):
		return UserTemps.objects.filter(user=self.request.user)

class ActiveSessionView(LoginRequiredMixin,ListView):
	template_name = 'health/active-session-view.html'
	# queryset = UserFeverSessions.objects.filter(active_session=True)
	context_object_name = 'activeSession'
	def get_queryset(self):
		return UserFeverSessions.objects.filter(active_session=True)
