import sys
import os
from core.base import MiBand2
from bluepy.btle import BTLEException
from django.utils import timezone

# PARENT DIRECTORY PATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medicalberry.settings")

import django
django.setup()

from heartguard.models import Device, Heartrate

# GET DEVICE
current_Device = Device.objects.get(id=1)

def send_to_db(rate):
    hr = Heartrate(device=current_Device, value=rate, event_time=timezone.now())
    hr.save()
    print(hr)

while True:
    try:
        band = MiBand2(current_Device.MAC_address, debug=True)
        band.setSecurityLevel(level="medium")
        band.authenticate()
        band.start_heart_rate_realtime(heart_measure_callback=send_to_db)
        band.disconnect()
    except BTLEException:
        pass
