from django.db import models

# Create your models here.

class Device(models.Model):
    name = models.CharField(max_length=200)
    MAC_address = models.CharField(max_length=17)

    def __str__(self):
        return '%s' % (self.name)

class Heartrate(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=3, decimal_places=0)
    event_time = models.DateTimeField('time of event')

    def __str__(self):
        return '%s %s' % (self.device, self.value)