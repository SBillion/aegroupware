from django.db import models
from planner.models import Event
from agency.models import Customer


class Session(models.Model):
	customer = models.ForeignKey(Customer)
	event = models.ForeignKey(Event, related_name='sessions')
	mark = models.IntegerField(blank=True, null=True)
	comment = models.CharField(max_length=255, blank=True, null=True)

	def __unicode__(self):
		return 'Session du %s' % (self.event.start)

