from django.contrib import admin
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Avg, F
from django.db.models.functions import TruncMinute
import json


from .models import Device, Kontrakton, DeviceType, Gas

# Register your models here.

class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'MAC_address')

    search_fields = ['id', 'name', 'MAC_address']
    
class KontraktonAdmin(admin.ModelAdmin):
    readonly_fields = ('device_type',)
    
    list_display = ('id', 'device', 'device_type', 'value', 'event_time',)
    
    list_filter = ['event_time']
    
    search_fields = ['id', 'device_name', 'value']
    
    def changelist_view(self, request, extra_context=None):
        chart_data = (
            Kontrakton.objects.annotate(date=TruncMinute("event_time"))
            .values("date")
            .annotate(y=Avg("value"))
            .order_by("-date")
        )
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data":as_json}
        
        return super().changelist_view(request, extra_context=extra_context)
        
class GasAdmin(admin.ModelAdmin):
    readonly_fields = ('device_type',)
    
    list_display = ('id', 'device', 'device_type', 'value', 'event_time',)
    
    list_filter = ['event_time']
    
    search_fields = ['id', 'device_name', 'value']
    
    def changelist_view(self, request, extra_context=None):
        chart_data = (
            Gas.objects.annotate(date=TruncMinute("event_time"))
            .values("date")
            .annotate(y=Avg("value"))
            .order_by("-date")
        )
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data":as_json}
        
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Kontrakton, KontraktonAdmin)
admin.site.register(Gas, KontraktonAdmin)
admin.site.register(Device, DeviceAdmin)

admin.site.register(DeviceType)