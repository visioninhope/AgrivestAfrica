from django.contrib import admin
from .models import TradeInvoice,TradeLog,TradeReceipt,FarmInvoice,FarmLog

class TradeReceiptsAdmin(admin.ModelAdmin):
    list_display =('trade','token','status','timestamp')
    readonly_fields = ('trade','token','paylink','status','timestamp')
    class Meta:
      model = TradeReceipt


admin.site.register(TradeInvoice)
admin.site.register(TradeLog)
admin.site.register(TradeReceipt, TradeReceiptsAdmin)

admin.site.register(FarmInvoice)
admin.site.register(FarmLog)