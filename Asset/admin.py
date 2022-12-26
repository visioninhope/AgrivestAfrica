from django.contrib import admin
from .models import Trade,Farm,Market


class TradeAdmin(admin.ModelAdmin):
  readonly_fields = ('slug',)
  class Meta:
    model = Trade

class FarmAdmin(admin.ModelAdmin):
  readonly_fields = ('slug',)
  class Meta:
    model = Farm

class MarketAdmin(admin.ModelAdmin):
  readonly_fields = ('slug',)
  class Meta:
    model = Market

admin.site.register(Trade, TradeAdmin)
admin.site.register(Farm, FarmAdmin)
admin.site.register(Market, MarketAdmin)