from django.contrib import admin
from .models import Trade,Partner,Farm,Produce


class TradeAdmin(admin.ModelAdmin):
  readonly_fields = ('slug',)
  class Meta:
    model = Trade

class PartnerAdmin(admin.ModelAdmin):
  readonly_fields = ('slug',)
  list_display = ('id','name','email','contact','date_joined')
  class Meta:
    model = Partner

class FarmAdmin(admin.ModelAdmin):
  readonly_fields = ('slug',)
  class Meta:
    model = Farm

class ProduceAdmin(admin.ModelAdmin):
  readonly_fields = ('slug',)
  class Meta:
    model = Produce

admin.site.register(Trade, TradeAdmin)
admin.site.register(Partner,PartnerAdmin)
admin.site.register(Farm, FarmAdmin)
admin.site.register(Produce, ProduceAdmin)