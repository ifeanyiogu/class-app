from django.contrib import admin

# Register your models here.

from django.core.exceptions import ValidationError
from django.db import transaction
from .models import ClassSession, Lecture, File, Image

class LectureInline(admin.TabularInline):
    model = Lecture
    fields = ['topic','note']
    extra = 1  # show one empty row
    min_num = 1  # enforce at least one at form validation level
    validate_min = True  # Django 2.1+ supports this

class SessionAdmin(admin.ModelAdmin):
    inlines = [LectureInline]
    list_display = ["id", "classroom__name", "lecture__topic", "is_published", "date"]
    ordering = ("-date",)

    def save_model(self, request, obj, form, change):
        # No need to validate here; validation happens in formset
        super().save_model(request, obj, form, change)

    def save_related(self, request, form, formsets, change):
        # Wrap entire save in atomic to ensure session + lectures are all-or-nothing
        with transaction.atomic():
            super().save_related(request, form, formsets, change)

    def clean(self):
        # Not typically used here; inline formset handles lecture existence
        pass

    def get_form(self, request, obj=None, **kwargs):
        # Optionally you can customize form to add cross-field validation
        return super().get_form(request, obj, **kwargs)


class LectureAdmin(admin.ModelAdmin):
    list_display = ["topic", "session__classroom__name", "session__date"]
    ordering = ("-session__date",)
    
class ImageAdmin(admin.ModelAdmin):
    list_display = ["session__lecture__topic", "tag", "content_type", "object_id",]
    filtering = ("session",)
    

class FileAdmin(admin.ModelAdmin):
    list_display = ["session__lecture__topic", "tag", "content_type", "object_id",]
    filtering = ("session",)

admin.site.register(ClassSession, SessionAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Lecture, LectureAdmin)
