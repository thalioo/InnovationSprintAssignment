# InnovationSprintAssignment
This is the implementation for the project assigned by InnovationSprintAssignment. Implements the procedure of allowing a user to sign up,login,and track health via submitting body temperatures. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine, and explaining the general functionality of the api.

## Prerequisites

In order to run this project python and django are required.
*[Python](https://www.python.org/downloads/) - Install latest python. Dont forget to add python to systempath
* Django framework
```
python -m pip install Django
```
* SQLite3 as a database

## About the Django Framework
This REST-API was implemented using the Django Framework. 
In this particular framework the models are the representation of the database.A model is the single, definitive source of information about your data. It contains the essential fields and behaviors of the data you’re storing. Generally, each model maps to a single database table.
The forms are classes that allow displaying a form which can display CRUD operations.GET and POST are the only HTTP methods to use when dealing with forms.
Views are the place where the implementations of the CRUD operations are implemented.A view is a “type” of Web page in your Django application that generally serves a specific function and has a specific template. 
Moreover the projects implementation is stored in the Django App health.
### Models
Our Model consists of four Models.(/InnovationSprintAssignment/health/models.py)
* User : Inherits Djangos contrib.auth.models that allows authorization for user logging.
  * username : Unique charfield
  * email : users registered password
  * password :  hashed represantation of the password
  * id : unique id of user
* UserTemps : Stores all temperatures for each user
  * user : type = reference of User Object,foreign key of User
  * timestamp : type = DateTimeField description =temperature submittion
  * temperature : type = floatField min=35,max=42
  * current_health : type =enum[HEALTH {if temperature<37},ONGOINGFEVER{if temperature>=37}]
  * active : type = BooleanField,description=True if is latest temperature submitted
  * primary_key = (user,timestamp)
* UserFeverSessions: Stores all Fever Sessions for each User
  * user : reference of User Object,foreign key of User
  * startTime :type = DateTimeField,description =start date-time of fever session
  * endTime = DateTimeField,description end date-time of fever session
  * active_session = BooleanField,description= True if session active
  * primary_key = (user,startTime)
### Forms(/InnovationSprintAssignment/health/forms.py)
* TempsForm Inherits UserTemps Model. Allows adding a temperature for the user submitting the form
* UserForm Inherits the User Model. Allows User to register
* UserProfileForm Inherits User Model. Allows User to view and edit profile
* SelectedSessionsForm Simple form to display sessions between two dates.
### Views (/InnovationSprintAssignment/health/views.py)
* profile Profile request if user is authenticated(GET)
* register User Registration(POST) 
* user_login User Login(POST)
* AddTempCreateView Add Temperature if user is authenticated(POST).If post is valid user is redirected to profile page.
* SessionView View Session between two dates. Return all session between two dates. Return session are checked for both start time and end time(GET).The return type is a json with
{id : {
	"sessionid"
	"temps" = []
	"user" 
	"startTime"
	"endTime"
}}
To retrieve the temperatures included in a fever session, we select all temperatures btween startTime and endTime.
*  TemperatureView View all submitted temperatures(GET)
* ActiveSessionView View Active Session if exists(GET)
## Urls
* (/) Index Displays the Projects Index
* (/health) The health App, and nested inside : <br />
(/login/) views.user_login , description = login of user<br />
(register/),views.register,description = registration<br />
(add_temperature/),views.AddTempCreateView,description = adds temperature<br />
<img src = images/AddTemp.JPG width=200><br />
(profile/),views.profile,description=shows profile<br />
<img src = images/profile.JPG width=200><br />
(view_temperatures/),views.TemperatureView,description=view all temperatures<br />
<img src = images/viewTemps.JPG width=200><br />
(view_active_session/),views.ActiveSessionView,description=view active fever session<br />
(view_sessions_dates/),views.SessionView,description =view session between two date<br />
<img src = images/findSessions.JPG width=200>

## Running the project
Navigate to InnovationSprintAssignment\InnovationSprintAssignment where manage.py is located and run :
```
python manage.py runserver
```
Locate to local host. REgister and try the API!
