"""
URL configuration for clinica project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from app.Employees.views import CustomTokenObtainPairView


schema_view = get_schema_view(openapi.Info(
    title="APIREST Clinica",
    default_version='v1',
    description="Clinica APIREST", contact=openapi.Contact(email="manuela.ruiz13@correo.tdea.edu.co"),
 
    ),
    public=True,
   
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/', include('app.api.routers')),
    path('documentation/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
