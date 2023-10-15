from Log.models import User
from Asset.models import Partner,Trade,Farm,Produce
from .models import TradeInvoice,FarmInvoice,ProduceInvoice
import graphene
from graphene_django import DjangoObjectType,DjangoListField

class UserData(DjangoObjectType):
   class Meta:
      model = User

class PartnerData(DjangoObjectType):
   class Meta:
      model = Partner

class TradeData(DjangoObjectType):
   class Meta:
      model = Trade

class TradeInvoiceData(DjangoObjectType):
  class Meta:
      model = TradeInvoice

class FarmData(DjangoObjectType):
   class Meta:
      model = Farm

class FarmInvoiceData(DjangoObjectType):
   class Meta:
      model = FarmInvoice

class ProduceData(DjangoObjectType):
   class Meta:
      model = Produce

class ProduceInvoiceData(DjangoObjectType):
   class Meta:
      model = ProduceInvoice

class Query(graphene.ObjectType):
   all_users = DjangoListField(UserData)
   all_partners = DjangoListField(PartnerData)    
   all_trades = DjangoListField(TradeData)
   all_trade_invoices= DjangoListField(TradeInvoiceData)
   all_farms = DjangoListField(FarmData)
   all_farm_invoices = DjangoListField(FarmInvoiceData)
   all_produces = DjangoListField(ProduceData)
   all_produce_invoices = DjangoListField(ProduceInvoiceData)

schema = graphene.Schema(query=Query)