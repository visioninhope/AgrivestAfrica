from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='homepage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/profile/', views.profile, name='profile_page'),
    path('dashboard/overview', views.dash_overview, name='dash_overview'),
    path('dashboard/transactions', views.dash_transactions, name='dash_transactions'),
    path('dashboard/produce', views.dash_produce, name='dash_produce'),

    
    path('about/', views.about, name='about_page'),
    path('advisors/', views.advisors, name='advisors_page'),
    path('board/', views.board, name='board_page'),
    path('faq/', views.faq, name='faq_page'),
    path('gallery/', views.gallery, name='gallery_page'),
    path('get_started/', views.get_started, name='get_started_page'),
    path('team/', views.team, name='team_page'),
    path('traction/', views.traction, name='traction_page'),
    path('webinar/', views.webinar, name='webinar_page'),
    path('what_we_do/', views.what_we_do, name='what_we_do_page'),

]