from django.contrib import admin
from .models import ClassRoom, ClassMember
# Register your models here.
class ClassMemberAdmin(admin.ModelAdmin):
    list_display = ["user__username", "classroom__name", "is_approved", "role", "date"]
    ordering = ["-date"]
    
    
class ClassAdmin(admin.ModelAdmin):
    list_display = ["name", "room_id", "creator__username", "date"]
    ordering = ["-date"]
    

admin.site.register(ClassRoom, ClassAdmin)
admin.site.register(ClassMember, ClassMemberAdmin)