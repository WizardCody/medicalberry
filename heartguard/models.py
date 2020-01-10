from django.db import models

# Create your models here.

class Patient(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    
    #mail = models.CharField(max_length=255)
    #phone = models.CharField(max_length=255)
    
    min_heartrate = models.DecimalField(max_digits=3, decimal_places=0)
    max_heartrate = models.DecimalField(max_digits=3, decimal_places=0)
    
    notify_mail = models.BooleanField(default=True)
    notify_telegram = models.BooleanField(default=True)
    
    def __str__(self):
        return '%s %s' % (self.name, self.surname)

class DeviceType(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return '%s' % (self.name)

class Device(models.Model):
    name = models.CharField(max_length=200)
    type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    MAC_address = models.CharField(max_length=17)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    
    def __str__(self):
        return '%s' % (self.name)

class Heartrate(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=3, decimal_places=0)
    event_time = models.DateTimeField('time of event')
    status = models.BooleanField(default=True)

    def device_type(self):
        return self.device.type
    device_type.short_description = 'Type'
    
    def __str__(self):
        return '%s %s' % (self.device, self.value)