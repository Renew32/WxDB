from django.urls import path,include
from .views import list_presta, PrestaViewSet, login_view, export_presta_to_excel
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'prestataires',PrestaViewSet)

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('prestataires/', list_presta, name='liste_prestataires'),
    path('api/', include(router.urls)),
    path('login/', login_view, name='login'),
    path('export-excel/', export_presta_to_excel, name='export_presta_excel'),
    
]
