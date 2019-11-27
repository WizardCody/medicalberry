from django.db import models

# Create your models here.

class Device(models.Model):
    name = models.CharField(max_length=200)
    MAC_address = models.CharField(max_length=17)

    def __str__(self):
        return '%s' % (self.name)