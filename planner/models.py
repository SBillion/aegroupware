# -*-coding:utf-8 -*
from django.db import models
from agency.models import Vehicle, Agency
from django.contrib.auth.models import User


EVENT_TYPE = (
	('code', 'Session de code'),
	('driving', 'Conduite en circulation'),
	('plateau', 'Conduite sur plateau'),
	('code_exam', 'Examen de code'),
	('driving_exam', 'Examen de conduite'),
	('initial_circuit', 'Conduite sur circuit (initial)'),
	('medium_circuit', 'Conduite sur circuit (intermédiaire)'),
	('improvement_circuit', 'Conduite sur circuit (perfectionnement)'),
)

class Event(models.Model):
	start = models.DateTimeField()
	end = models.DateTimeField()
	slots = models.IntegerField()
	type = models.CharField(max_length=255, choices=EVENT_TYPE)
	vehicle = models.ManyToManyField(Vehicle, null=True, blank=True, related_name='events')
	agency = models.ForeignKey(Agency)
	supervisor = models.ForeignKey(User)

	def __unicode__(self):
		return 'Evenement du %s au %s' % (self.start, self.end)
