from django.contrib import admin
from .models import User,Sponsor,Farmer,Offtaker

admin.site.register(User)
admin.site.register(Sponsor)
admin.site.register(Farmer)
admin.site.register(Offtaker)
