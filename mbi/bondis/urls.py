from rest_framework.routers import DefaultRouter
from .views import ResultadosEsperaViewSet

router = DefaultRouter()
router.register(r'resultados', ResultadosEsperaViewSet, base_name='resultados')
urlpatterns = router.urls