from django.contrib import admin
from .models import Trade,Partner,Farm,Market


class TradeAdmin(admin.ModelAdmin):
  readonly_fields = ('slug',)
  class Meta:
    model = Trade

class PartnerAdmin(admin.ModelAdmin):
  readonly_fields = ('slug',)
  list_display = ('name','email','contact','date_joined')
  class Meta:
    model = Partner

class FarmAdmin(admin.ModelAdmin):
  readonly_fields = ('slug',)
  class Meta:
    model = Farm

class MarketAdmin(admin.ModelAdmin):
  readonly_fields = ('slug',)
  class Meta:
    model = Market

admin.site.register(Trade, TradeAdmin)
admin.site.register(Partner,PartnerAdmin)
admin.site.register(Farm, FarmAdmin)
admin.site.register(Market, MarketAdmin)