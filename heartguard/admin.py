from django.contrib import admin

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Avg, F
from django.db.models.functions import TruncMinute
import json


from .models import Heartrate, Device

# Register your models here.
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('name', 'MAC_address')

    search_fields = ['name', 'MAC_address']

class HeartrateAdmin(admin.ModelAdmin):
    list_display = ('device', 'value', 'event_time')

    list_filter = ['event_time']

    search_fields = ['device__name', 'value']
	
    def changelist_view(self, request, extra_context=None):
    
        chart_data = (
            Heartrate.objects.annotate(date=TruncMinute("event_time"))
            .values("date")
            .annotate(y=Avg("value"))
            .order_by("-date")
        )
    
        # Serialize and attach the chart data to the template context
        as_json = json.dumps(list(chart_data), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data": as_json}
        
        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)

admin.site.register(Heartrate, HeartrateAdmin)
admin.site.register(Device, DeviceAdmin)
