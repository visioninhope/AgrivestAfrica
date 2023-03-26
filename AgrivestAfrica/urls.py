from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
# import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('Home.urls')),
    path('',include('Log.urls')),
    path('',include('Transaction.urls')),
    path('',include('allauth.urls')),
    # path('__debug__/', include('debug_toolbar.urls')),
    path('robots.txt', include('robots.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


