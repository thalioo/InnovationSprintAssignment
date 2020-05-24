# InnovationSprintAssignment
This is the implementation for the project assigned by InnovationSprintAssignment. Implements the procedure of allowing a user to sign up,login,and track health via submitting body temperatures. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

## Prerequisites

In order to run this project python and django are required.
*[Python](https://www.python.org/downloads/) - Install latest python. Dont forget to add python to systempath
* Django framework
```
python -m pip install Django
```
* SQLite3 as a database

## About the Django Framework
This REST-API was implemented using the Django Framework. In this particular framework the models are the representation of the database.
The forms are classes that allow displaying a form which can display CRUD operations.
Views are the place where the implementations of the CRUD operations are implemented.
Moreover the projects implementation is stored in the Django App health.
### Models
Our Model consists of four Models.(/InnovationSprintAssignment/health/models.py)
* User : Inherits Djangos contrib.auth.models that allows authorization for user logging.
	** username : Unique charfield **
	** email : users registered password**
	** password :  hashed represantation of the password**
	** id : unique id of user**
* UserTemps : Stores all temperatures for each user	**
	** user : type = reference of User Object,foreign key of User**
	** timestamp : type = DateTimeField description =temperature submittion**
	** temperature : type = floatField min=35,max=42**
	** current_health : type =enum[HEALTH {if temperature<37},ONGOINGFEVER{if temperature>=37}] **
	** active : type = BooleanField,description=True if is latest temperature submitted**
	** primary_key = (user,timestamp)**
* UserFeverSessions: Stores all Fever Sessions for each User
	** user : reference of User Object,foreign key of User**
	** startTime :type = DateTimeField,description =start date-time of fever session**
	** endTime = DateTimeField,description end date-time of fever session**
	** active_session = BooleanField,description= True if session active**
### Forms(/InnovationSprintAssignment/health/forms.py)
*TempsForm Inherits UserTemps Model. Allows adding a temperature for the user submitting the form
*UserForm Inherits the User Model. Allows User to register
*UserProfileForm Inherits User Model. Allows User to view and edit profile
*SelectedSessionsForm Simple form to display sessions between two dates.
### Views
*profile Profile request if user is authenticated(GET)
*register User Registration(POST) 
*user_login User Login(POST)
*AddTempCreateView Add Temperature if user is authenticated(POST).If post is valid user is redirected to profile page.
*SessionView View Session between two dates. Return all session between two dates. Return session are checked for both start time and end time(GET).The return type is a json with
{id : {
	"sessionid"
	"temps" = []
	"user" 
	"startTime"
	"endTime"
}}
To retrieve the temperatures included in a fever session, we select all temperatures btween startTime and endTime.s
*TemperatureView View all submitted temperatures(GET)
*ActiveSessionView View Active Session if exists(GET)
## Urls
* (/) Index Displays the Projects Index
* (/health) The health App, and nested inside : 
	**('/login/') views.user_login , description = login of user**
    **('register/'),views.register,description = registration**
    **('add_temperature/'),views.AddTempCreateView,description='add_temperature'**
    ![images/AddTemp.JPG]
    **('profile/'),views.profile,name='profile'**
    ![images\profile.JPG]
    **('view_temperatures/'),views.TemperatureView,description='view_temperatures'**
    ![IMAGES/viewTemps.JPG]
    **('view_active_session/)',views.ActiveSessionView,description='view_active_session'**
    **('view_sessions_dates/'),views.SessionView,description ='view_sessions_dates' **
    ![\images\findSessions.JPG]

## Running the project
Navigate to InnovationSprintAssignment\InnovationSprintAssignment where manage.py is located and run :
```
python manage.py runserver
```
Locate to 