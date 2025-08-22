from django.contrib import admin
from .models import Comment, Reply
# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user__username', 'note']
    ordering = ('-date',)

class ReplyAdmin(admin.ModelAdmin):
    list_display = ['comment__note', 'user__username', 'note']
    ordering = ['-date']
 
admin.site.register(Reply, ReplyAdmin)    
admin.site.register(Comment, CommentAdmin)