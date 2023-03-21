from django.contrib import admin
from .models import TradeInvoice,FarmInvoice,ProduceInvoice

admin.site.register(TradeInvoice)

admin.site.register(FarmInvoice)

admin.site.register(ProduceInvoice)