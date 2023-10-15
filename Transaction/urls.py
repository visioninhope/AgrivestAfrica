from django.urls import path
from . import views
from graphene_django.views import GraphQLView
from .schema import schema
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('trades/',views.trades,name='trades_page'),
    path('makeTrade/<str:slug>/', views.makeTrade, name='makeTrade_page' ),
    path('farms/',views.farms,name='farms_page'),
    path('makeFarm/<str:slug>/', views.makeFarm, name='makeFarm_page' ),
    path('produce/', views.produce, name='produce_page'),
    path('buyProduce/<str:slug>/', views.buy_produce, name='buyProduce_page'),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
]