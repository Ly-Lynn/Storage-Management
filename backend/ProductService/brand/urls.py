from .views import BrandViews
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'product/brands', BrandViews)
urlpatterns = router.urls