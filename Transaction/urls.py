from django.urls import path
from . import views

urlpatterns = [
    path('trades/',views.trades,name='trades_page'),
    path('makeTrade/<str:slug>/', views.makeTrade, name='makeTrade_page' ),
    path('farms/',views.farms,name='farms_page'),
    path('makeFarm/<str:slug>/', views.makeFarm, name='makeFarm_page' ),
    path('markets/', views.markets, name='markets_page'),
    path('callback', views.callback, name='callback_page'),
]