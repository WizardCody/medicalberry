import os, sys

# PARENT DIRECTORY PATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medicalberry.settings")

import django
django.setup()

from homeguard.models import Device, DeviceType, Gas

# PRINT ALL HEARTRATES
print(Gas.objects.all())

# GET DEVICE
#print(current_Device)
# INSERT HEARTRATE
from django.utils import timezone

DeviceType(name='Gas').save()
temp = DeviceType.objects.get(pk=1)
print(temp)
Device(name='MQ7', type=temp, MAC_address='5a:93:fc:93:a1:59').save()
current_Device = Device.objects.get(pk=1)
print(current_Device)
Gas(device=current_Device, value=45.24, event_time=timezone.now()).save()