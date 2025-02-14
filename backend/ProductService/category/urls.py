from .views import CategoryViews
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'product/categories', CategoryViews)
urlpatterns = router.urls
