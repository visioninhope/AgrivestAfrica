from django.contrib import admin 
from .models import Inbox,Team,Board,Advisor

class InboxAdmin(admin.ModelAdmin):
    list_display = ('title','author','date_posted')

admin.site.register(Inbox,InboxAdmin)

admin.site.register(Team)
admin.site.register(Board)
admin.site.register(Advisor)