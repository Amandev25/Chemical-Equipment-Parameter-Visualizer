"""
Tests for API endpoints.
"""
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Equipment, CSVUpload, DataSummary


class EquipmentAPITestCase(APITestCase):
    """
    Test cases for Equipment API endpoints.
    """
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        # Create sample equipment
        self.equipment1 = Equipment.objects.create(
            equipment_id='PUMP-001',
            equipment_name='Main Pump',
            equipment_type='Pump',
            flowrate=150.5,
            status='Active'
        )
        
        self.equipment2 = Equipment.objects.create(
            equipment_id='VALVE-001',
            equipment_name='Control Valve',
            equipment_type='Valve',
            flowrate=100.0,
            status='Active'
        )
    
    def test_list_equipment(self):
        """Test listing all equipment."""
        url = reverse('api:equipment-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_retrieve_equipment(self):
        """Test retrieving a single equipment."""
        url = reverse('api:equipment-detail', kwargs={'pk': self.equipment1.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['equipment_id'], 'PUMP-001')
    
    def test_filter_equipment_by_type(self):
        """Test filtering equipment by type."""
        url = reverse('api:equipment-list')
        response = self.client.get(url, {'type': 'Pump'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['equipment_type'], 'Pump')
    
    def test_search_equipment(self):
        """Test searching equipment by name or ID."""
        url = reverse('api:equipment-list')
        response = self.client.get(url, {'search': 'Main'})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)


class DashboardAPITestCase(APITestCase):
    """
    Test cases for Dashboard API endpoints.
    """
    
    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        
        # Create sample equipment
        Equipment.objects.create(
            equipment_id='PUMP-001',
            equipment_name='Main Pump',
            equipment_type='Pump',
            flowrate=150.5,
            status='Active'
        )
    
    def test_dashboard_summary(self):
        """Test dashboard summary endpoint."""
        url = reverse('api:dashboard-summary')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_equipment', response.data)
        self.assertEqual(response.data['total_equipment'], 1)
    
    def test_flowrate_chart_data(self):
        """Test flowrate chart data endpoint."""
        url = reverse('api:flowrate-chart')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('equipment_ids', response.data)
        self.assertIn('flowrates', response.data)
    
    def test_type_distribution_data(self):
        """Test type distribution data endpoint."""
        url = reverse('api:type-distribution')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('types', response.data)
        self.assertIn('counts', response.data)


class HealthCheckTestCase(APITestCase):
    """
    Test case for health check endpoint.
    """
    
    def test_health_check(self):
        """Test API health check."""
        url = reverse('api:health-check')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'healthy')

