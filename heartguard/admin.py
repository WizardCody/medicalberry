from django.contrib import admin

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Avg, F, Min, Max
from django.db.models.functions import TruncMinute
import json

from django.utils.html import format_html

from django.db.models import Q

from .models import Patient, Heartrate, Device, DeviceType


class PatientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'surname')
    list_display_links = list_display

    search_fields = ['id', 'name', 'surname']
    
    ordering = ('id',)
    
    fieldsets = (
        (None, {
            'fields' : ('name', 'surname')}),
        ('medical information', {
            'classes': ('callapse',),
            'fields' : ('min_heartrate', 'max_heartrate', 'notify_mail', 'notify_telegram')
        }),
    )
    

class DeviceTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = list_display

    search_fields = ['id', 'name']
    
    ordering = ('id',)
    
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'MAC_address', 'patient')
    list_display_links = list_display

    search_fields = ['id', 'name', 'type__name', 'MAC_address', 'patient']
    
    ordering = ('id',)

class HeartrateAdmin(admin.ModelAdmin):
    
    fields = ('device', 'device_type', 'value', 'event_time', 'status_parsed')
    readonly_fields = ('device_type', 'status1')
    
    list_display = ('id', 'device', 'device_type', 'value', 'event_time', 'patient', 'status1')
    list_display_links = list_display

    list_filter = ['event_time']
    
    search_fields = ['id', 'device__name', 'value']
    
    ordering = ('-id',)
    
    def patient(self, obj):
        return obj.device.patient
    patient.short_description = "patient"
    
    def status1(self, obj):
    
        if (obj.status == True):
            return format_html('<font color="lightgreen">OK</font>')
        else:
            return format_html('<font color="red">WARNING</font>')
            
    status1.short_description = "status"
	
    
    
    
    def changelist_view(self, request, extra_context=None):
    
        query = request.GET.get('q')
        if not query:
            results = Heartrate.objects
        else:
            results = Heartrate.objects.filter(Q(id__icontains=query) | Q(value__icontains=query))
    
        chart_data_avg = (
            results.annotate(date=TruncMinute("event_time"))
            .values("date")
            .annotate(y=Avg("value"))
            .order_by("-date")
        )
        
        chart_data_min = (
            results.annotate(date=TruncMinute("event_time"))
            .values("date")
            .annotate(y=Min("value"))
            .order_by("-date")
        )
        
        chart_data_max = (
            results.annotate(date=TruncMinute("event_time"))
            .values("date")
            .annotate(y=Max("value"))
            .order_by("-date")
        )
    
        # Serialize and attach the chart data to the template context
        as_json1 = json.dumps(list(chart_data_avg), cls=DjangoJSONEncoder)
        as_json2 = json.dumps(list(chart_data_min), cls=DjangoJSONEncoder)
        as_json3 = json.dumps(list(chart_data_max), cls=DjangoJSONEncoder)
        extra_context = extra_context or {"chart_data_avg": as_json1, "chart_data_min": as_json2, "chart_data_max": as_json3}
        
        # Call the superclass changelist_view to render the page
        return super().changelist_view(request, extra_context=extra_context)
        #return super().queryset(request, queryset)

admin.site.register(Patient, PatientAdmin)
admin.site.register(Heartrate, HeartrateAdmin)
admin.site.register(Device, DeviceAdmin)
admin.site.register(DeviceType, DeviceTypeAdmin)

