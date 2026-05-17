from rest_framework_nested import routers
from .views import ProprietarioViewSet, ImovelViewSet, FotoImovelViewSet

router = routers.DefaultRouter()
router.register(r'proprietarios', ProprietarioViewSet, basename='proprietarios')
router.register(r'imoveis', ImovelViewSet, basename='imoveis')

imoveis_router = routers.NestedDefaultRouter(router, r'imoveis', lookup='imovel')
imoveis_router.register(r'fotos', FotoImovelViewSet, basename='imovel-fotos')

urlpatterns = router.urls + imoveis_router.urls