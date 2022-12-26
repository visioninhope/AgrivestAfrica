from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='homepage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/profile/', views.profile, name='profile_page'),
]