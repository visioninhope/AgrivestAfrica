from django.urls import path
from . import views

urlpatterns = [
    path('trades/',views.trades,name='trades_page'),
    path('makeTrade/<int:id>/', views.makeTrade, name='makeTrade_page' ),
    path('farms/',views.farms,name='farms_page'),
    path('makeFarm/<int:id>/', views.makeFarm, name='makeFarm_page' ),
    path('markets/', views.markets, name='markets_page'),

    path('callback', views.callback, name='callback_page'),
]