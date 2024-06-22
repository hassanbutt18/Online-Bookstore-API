# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from bookstore.views import BookViewSet ,AuthorViewSet ,CategoryViewSet ,CartViewSet ,OrderItemViewSet



from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Online book store",
      default_version='v1',
      description="Online book store apis",
      contact=openapi.Contact(email="contact@hassan.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'author', AuthorViewSet)
router.register(r'category', CategoryViewSet)
router.register(r'cart', CartViewSet)
router.register(r'order-items', OrderItemViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
