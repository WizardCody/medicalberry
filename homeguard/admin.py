from django.contrib import admin

from .models import Device

# Register your models here.

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'MAC_address')

    search_fields = ['name', 'MAC_address']

admin.site.register(Device, DeviceAdmin)