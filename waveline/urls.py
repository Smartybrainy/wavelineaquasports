from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
    path('blog/', include('blog.urls', namespace='blog')),
    path('accounts/', include('accounts.urls', namespace="accounts")),
    path('gallery/', include('gallery.urls', namespace='gallery')),
    # For password reset
    path('accounts/', include('django.contrib.auth.urls')),
    path('favicon/', RedirectView.as_view(url=staticfiles_storage.url('fav/favicon.ico'))),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('sport.urls', namespace='sport')),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
