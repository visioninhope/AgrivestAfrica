from django.urls import path
from . import views

urlpatterns = [
    path('s_register/',views.s_register,name='s_register_page'),
    path('f_register/',views.f_register,name='f_register_page'),
    path('o_register/',views.o_register,name='o_register_page'),

    path('forgot_password/',views.forgot_password, name='forgot_password'),
    path('reset_password/<token>/', views.reset_password, name='reset_password'),

    path('login/', views.login_user, name='login_page'),
    path('logout/',views.logout_user, name='logout_page'),

    path('map/',views.map,name='map_page'),

    path('welcome', views.welcome),
    #path('mail/',views.mail, name='mail')
]