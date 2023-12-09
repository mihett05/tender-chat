from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    # urls for swagger (docs for backend API)
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='docs'),

    # urls for admin site (useless because concentrated on api dev)
    path('admin/', admin.site.urls),

    # urls for apps
    path('users/', include('users.urls')),
    # path('chats/', include('chats.urls')),
    path('auth/', include('authentication.urls')),
    path('', include(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))),
]