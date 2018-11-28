from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^bondis/', include('bondis.urls')),
    url(r'^', RedirectView.as_view(url='bondis/mapa/'), name='mapa_bondis'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
