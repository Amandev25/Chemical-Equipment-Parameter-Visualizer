"""
URL configuration for API endpoints.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EquipmentViewSet, CSVUploadViewSet,
    dashboard_summary, flowrate_chart_data, type_distribution_data,
    generate_report, clear_all_data, health_check,
    login_view, register_view, logout_view, current_user, get_csrf_token
)

# Create router for ViewSets
router = DefaultRouter()
router.register(r'equipment', EquipmentViewSet, basename='equipment')
router.register(r'uploads', CSVUploadViewSet, basename='csv-upload')

app_name = 'api'

urlpatterns = [
    # Router URLs
    path('', include(router.urls)),
    
    # Authentication endpoints
    path('auth/login/', login_view, name='login'),
    path('auth/register/', register_view, name='register'),
    path('auth/logout/', logout_view, name='logout'),
    path('auth/me/', current_user, name='current-user'),
    path('auth/csrf/', get_csrf_token, name='get-csrf-token'),
    
    # Dashboard endpoints
    path('dashboard/summary/', dashboard_summary, name='dashboard-summary'),
    path('dashboard/flowrate-chart/', flowrate_chart_data, name='flowrate-chart'),
    path('dashboard/type-distribution/', type_distribution_data, name='type-distribution'),
    
    # Report generation
    path('reports/generate/', generate_report, name='generate-report'),
    
    # Utility endpoints
    path('health/', health_check, name='health-check'),
    path('clear/', clear_all_data, name='clear-all-data'),
]

