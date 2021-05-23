from django.contrib import admin
from mainApp.models import *

admin.site.site_header = "교통약자 안전 승하차 솔루션, 틈"
admin.site.site_title = '교통약자 안전 승하차 솔루션, 틈'
admin.site.index_title = '관리자 페이지'


class StationAdmin(admin.ModelAdmin):
    list_display = ('line', 'name', 'foothold', 'platform')
    list_display_links = ('name',)
    list_filter = ('line',)


admin.site.register(Station, StationAdmin)


class DoorAdmin(admin.ModelAdmin):
    list_display = ('station', 'car_number', 'door_number', 'distance')
    list_display_links = ('station',)
    list_filter = ('station__name',)


admin.site.register(Door, DoorAdmin)


class ComplexityAdmin(admin.ModelAdmin):
    list_display = ('station', 'day')
    list_display_links = ('station',)
    list_filter = ('station__name',)


admin.site.register(Complexity, ComplexityAdmin)


class TimeAdmin(admin.ModelAdmin):
    list_display = ('complex_id', 'time', 'complexity')
    list_display_links = ('complex_id',)
    list_filter = ('complex_id',)


admin.site.register(Time, TimeAdmin)


class FavoriteStationAdmin(admin.ModelAdmin):
    list_display = ('user', 'station')
    list_display_links = ('user',)
    list_filter = ('user__username',)


admin.site.register(FavoriteStation, FavoriteStationAdmin)
