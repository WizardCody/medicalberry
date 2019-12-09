import os, sys

# PARENT DIRECTORY PATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medicalberry.settings")

import django
django.setup()

from homeguard.models import Device, Kontrakton

# PRINT ALL HEARTRATES
print(Kontrakton.objects.all())

# GET DEVICE
current_Device = Device.objects.get(pk=1)

# INSERT HEARTRATE
from django.utils import timezone
Kontrakton(device=current_Device, value=True, event_time=timezone.now()).save()