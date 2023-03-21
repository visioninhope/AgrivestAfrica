from django.urls import path
from . import views

urlpatterns = [
    path('trades/',views.trades,name='trades_page'),
    path('makeTrade/<str:slug>/', views.makeTrade, name='makeTrade_page' ),
    path('farms/',views.farms,name='farms_page'),
    path('makeFarm/<str:slug>/', views.makeFarm, name='makeFarm_page' ),
    path('produce/', views.produce, name='produce_page'),
    path('buyProduce/<str:slug>/', views.buy_produce, name='buyProduce_page'),
]