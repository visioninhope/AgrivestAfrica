from django.contrib import admin 
from .models import Inbox

class InboxAdmin(admin.ModelAdmin):
    list_display = ('title','author','date_posted')

admin.site.register(Inbox,InboxAdmin)