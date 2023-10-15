from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='homepage'),
    path('dashboard/', views.dashboard, name='dashboard'),
    

    path('dashboard/profile/', views.profile, name='profile_page'),
    path('dashboard/inbox/',views.inbox, name='inbox_page'),
    path('dashboard/tradeLog', views.trade_log, name='tradeLog_page'),
    path('dashboard/tradeLog_info/<str:slug>', views.tradeLog_info, name='tradeLog_info'),
    path('dashboard/farmLog', views.farm_log, name='farmLog_page'),
    path('dashboard/farmLog_info/<str:slug>', views.farmLog_info, name='farmLog_info'),
    path('dashboard/produceLog', views.produce_log, name='produceLog_page'),
    path('dashboard/produceLog_info/<str:slug>/', views.produceLog_info, name='produceLog_info'),

    path('dashboard/overview', views.dash_overview, name='dash_overview'),

    path('dashboard/transactions', views.dash_transactions, name='dash_transactions'),
    path('dashboard/produce', views.dash_produce, name='dash_produce'),

    path('trans_callback/<str:slug>/', views.trans_callback),
    
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
    path('testimonials/', views.testimonials, name='testimonials_page'),
    path('referrals/', views.referrals, name='referrals_page'),
    path('investors/', views.investors, name='investors_page'),
    path('blog/', views.blog, name='blog_page'),
    path('contact', views.contact, name='contact_page'),
    path('how_to/', views.how_to, name='how_to_page'),
    path('terms_and_conditions', views.terms_and_conditions, name='terms_and_conditions_page'),
    path('blog_soya/',views.blog_soya, name='blog_soya_page'),

    path('mail/',views.mailPortal, name='mailPortal'),
    path('sitemap/', views.sitemap),

    path('logout', views.logout_user, name='logout'),
    path('testpay', views.testpay),

    path('cms_team', views.cms_team, name='cms_team_page'),
    path('cms_add_team', views.cms_add_team, name='cms_add_team_page'),
    path('cms_edit_team/<int:id>', views.cms_edit_team, name='cms_edit_team_page'),
    path('cms_board', views.cms_board, name='cms_board_page'),
    path('cms_add_board', views.cms_add_board, name='cms_add_board_page'),
    path('cms_edit_board/<int:id>', views.cms_edit_board, name='cms_edit_board_page'),
    path('cms_advisor', views.cms_advisor, name='cms_advisor_page'),
    path('cms_add_advisor', views.cms_add_advisor, name='cms_add_advisor_page'),
    path('cms_edit_advisor/<int:id>', views.cms_edit_advisor, name='cms_edit_advisor_page')

]