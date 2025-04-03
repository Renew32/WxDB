from django.urls import path,include
from .views import list_presta, PrestaViewSet, login_view, export_presta_to_excel
from rest_framework.routers import DefaultRouter
from . import views 
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'prestataires',PrestaViewSet)

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('prestataires/', list_presta, name='liste_prestataires'),
    path('api/', include(router.urls)),
    path('login/', login_view, name='login'),
    path('export-excel/', export_presta_to_excel, name='export_presta_excel'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
