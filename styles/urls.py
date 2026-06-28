from rest_framework.routers import DefaultRouter
from .views import StyleViewSet

router = DefaultRouter()
router.register(r"styles", StyleViewSet,basename="styles")

urlpatterns = router.urls