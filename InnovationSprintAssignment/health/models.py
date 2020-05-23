from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
# class UserProfile(models.Model):
# 	#Extend Djangos Built in User Model
# 	user = models.OneToOneField(User,on_delete=models.CASCADE)
# 	# The additional attributes we wish to include.
# 	website = models.URLField(blank=True)

# 	# Override the __unicode__() method to return out something meaningful!
# 	# Remember if you use Python 2.7.x, define __unicode__ too!
# 	def __str__(self):
# 		return self.user.username
# 	def __str__(self): # For Python 2, use __unicode__ too
# 		return self.title
class UserTemps(models.Model):
	#Define a many to one relationship with the UserProfile Model
	userId = models.ForeignKey(User, on_delete=models.CASCADE)
	temperature = models.FloatField(default=36.6,
        validators=[MaxValueValidator(42), MinValueValidator(35)])
	timeStamp = models.DateTimeField('date-time of temperature')
	active = models.BooleanField(default=False)
	class Meta:
		#Creates mutliple key
		unique_together = (("userId","timeStamp"))

class UserFeverSessions(models.Model):
	# id = models.AutoField(User=True)
	userId = models.ForeignKey(User, on_delete=models.CASCADE)
	startTime = models.DateTimeField('start date-time of fever session')
	endTime = models.DateField('end date-time of fever session')
	def getActiveSession(self,date1,date2):
		return self.startTime>=date1,self.endTime<=date2
	
		