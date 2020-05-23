from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.urls  import reverse
from health.forms import UserForm,TempsForm
from django.shortcuts import render,get_object_or_404
from health.models import UserTemps,UserFeverSessions
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return HttpResponse("Hello, you are at the HealthApp HomePage")
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


def add_temperature(request):
	# A HTTP POST?
	if request.user.is_authenticated:
		if request.method == 'POST':
			print(request.user)
			form = TempsForm(data=request.POST)
			# current_user = User.objects.get(username=request.user)
			# Have we been provided with a valid form?
			if form.is_valid():
			# Save the new category to the database.
				# print(form.temperature)
				print(type(request.user))
				current_user = User.objects.get(pk=request.user).username
				form.user= current_user
				form.save()
				# form.user = current_user
				form.save(commit=True)
				if form.temperature>=37:
					updateFeverSession(form)
					setActiveStatus(form)
				
			# Now that the temp is saved
			# We could give a confirmation message
				return index(request)
			else:
				print('mpika')
				print(form.errors)
		# Will handle the bad form, new form, or no form supplied cases.
		# Render the form with error messages (if any).
		else: form = TempsForm()
		return render(request, 'health/add_temperature.html', {'form': form})
	else : 

		return login(request)
	# The supplied form contained errors -
	# just print them to the terminal.
def profile(request, username):
	try:
		user = User.objects.get(username=username)
	except User.DoesNotExist:
		return redirect('index')
	userprofile = UserProfile.objects.get_or_create(user=user)[0]
	form = UserProfileForm()
	if request.method == 'POST':
		form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
		if form.is_valid():
			form.save(commit=True)
			return redirect('profile', user.username)
		else:
			print(form.errors)
	return render(request, 'health/profile.html',
	{'userprofile': userprofile, 'form': form})
def updateFeverSession(form):
	session = UserFeverSessions
	return session

