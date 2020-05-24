from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
import datetime
class UserTemps(models.Model):
	#Define a many to one relationship with the UserProfile Model
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	temperature = models.FloatField(default=36.6,
        validators=[MaxValueValidator(42), MinValueValidator(35)])
	timeStamp = models.DateTimeField(default=datetime.datetime.now)
	HEALTHY = 'HEALTHY'
	FEVER = 'ONGOINGFEVER'
	STATUS = [ ('HEALTHY',_('Healthy')),
			('FEVER',_('Fever')),
		]

	current_health = models.CharField(
	    max_length=9,
	    choices=STATUS,
	    default=HEALTHY,
	)
	active = models.BooleanField(default=False)
	#Override Save to Set Active Status According to Temperature. 
	def save(self, *args, **kwargs):
		if self.temperature<37:
			self.current_health = 'HEALTHY'
		else: self.current_health = 'ONGOINGFEVER'
		super(UserTemps, self).save(*args, **kwargs)
	class Meta:
		#Creates mutliple key
		unique_together = (("user","timeStamp"))

class UserFeverSessions(models.Model):
	# id = models.AutoField(User=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	startTime = models.DateTimeField('start date-time of fever session')
	endTime = models.DateTimeField(null=True, blank=True,verbose_name='end date-time of fever session')
	active_session = models.BooleanField(default=False)
	class Meta:
		#Creates mutliple key
		unique_together = (("user","startTime"))
	def getActiveSession(self,date1,date2):
		return self.startTime>=date1,self.endTime<=date2
	
		