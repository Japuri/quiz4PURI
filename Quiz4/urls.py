from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    # Proper namespace registration
    path('auth/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('jobs/', include(('jobs.urls', 'jobs'), namespace='jobs')),
    path('', include(('posts.urls', 'posts'), namespace='posts')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
