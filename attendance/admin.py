from django.contrib import admin
from .models import Attendance
# Register your models here.
class AttendAdmin(admin.ModelAdmin):
    list_display = ['session__classroom__name', 'session__lecture__topic', 'user__username']
    
    ordering = ('-date',)
    
admin.site.register(Attendance, AttendAdmin)