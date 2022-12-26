from django.contrib import admin
from .models import TradeInvoice,TradeLog,FarmInvoice,FarmLog

admin.site.register(TradeInvoice)
admin.site.register(TradeLog)
admin.site.register(FarmInvoice)
admin.site.register(FarmLog)