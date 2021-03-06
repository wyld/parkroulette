from content.models import Log, Ticket, Path
from django.contrib.gis import admin


class LogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'address', 'week_day', 'from_time', 'to_time', 'type')
    list_filter = ('type',)


class TicketAdmin(admin.GeoModelAdmin):
    pass


class PathAdmin(admin.GeoModelAdmin):
     list_filter = ('valid',)


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Path, PathAdmin)
admin.site.register(Log, LogAdmin)