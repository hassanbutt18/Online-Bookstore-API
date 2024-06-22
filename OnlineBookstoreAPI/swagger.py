# OnlineBookstoreAPI/swagger.py

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Online Book Store",
      default_version='v1',
      description="Online Book Store",
      terms_of_service="https://www.example.com/policies/terms/",
      contact=openapi.Contact(email="contact@hassan.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
