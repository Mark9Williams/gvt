"""
URL configuration for alpha project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from brand.views import BrandViewSet
from store.views import StoreViewSet
from product.views import ProductViewSet
from inventory.views import StoreInventoryViewSet
from storeassignment.views import StoreAssignmentViewSet


router = DefaultRouter()
router.register(r'brands',BrandViewSet)
router.register(r'stores',StoreViewSet)
router.register(r'products',ProductViewSet)
router.register(r'storeassignments',StoreAssignmentViewSet)
router.register(r'storeinventory',StoreInventoryViewSet)

urlpatterns = [
    path("api/",include(router.urls)),
    path('admin/', admin.site.urls),
]
