from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import ResultadosEsperaViewSet, MapaDeColectivosView

router = DefaultRouter()
router.register(r'resultados', ResultadosEsperaViewSet, base_name='resultados')

urlpatterns = [
    url(r'^mapa/$', MapaDeColectivosView.as_view(), name='mapa'),
    ] + router.urls