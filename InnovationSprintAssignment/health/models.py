from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

class UserTemps(models.Model):
	#Define a many to one relationship with the UserProfile Model
	def setActiveStatus(temperature):
		HEALTHY = 'HEALTHY'
		FEVER = 'ONGOINGFEVER'
		if temperature>=models.FloatField(37) : 
			return HEALTHY
		else: 
			return FEVER
	userId = models.ForeignKey(User, on_delete=models.CASCADE)
	temperature = models.FloatField(default=36.6,
        validators=[MaxValueValidator(42), MinValueValidator(35)])
	timeStamp = models.DateTimeField('date-time of temperature')
	HEALTHY = 'HEALTHY'
	FEVER = 'ONGOINGFEVER'
	STATUS = [ ('HEALTHY',_('Healthy')),
			('FEVER',_('Fever')),
		]

	active_status = models.CharField(
	    max_length=8,
	    choices=STATUS,
	    default=setActiveStatus(temperature),
	)
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
	
		