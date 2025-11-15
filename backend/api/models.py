"""
Models for chemical equipment data management.
"""
from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.auth.models import User


class CSVUpload(models.Model):
    """
    Model to track CSV file uploads.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='csv_uploads',
        null=True,
        blank=True
    )
    file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    total_records = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'CSV Upload'
        verbose_name_plural = 'CSV Uploads'
    
    def __str__(self):
        return f"{self.filename} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"


class Equipment(models.Model):
    """
    Model to store individual equipment data parsed from CSV.
    """
    EQUIPMENT_TYPES = [
        ('Pump', 'Pump'),
        ('Valve', 'Valve'),
        ('Tank', 'Tank'),
        ('Reactor', 'Reactor'),
        ('Heat Exchanger', 'Heat Exchanger'),
        ('Compressor', 'Compressor'),
        ('Separator', 'Separator'),
        ('Mixer', 'Mixer'),
        ('Filter', 'Filter'),
        ('HeatExchanger', 'HeatExchanger'),
        ('Condenser', 'Condenser'),
        ('Other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Maintenance', 'Maintenance'),
        ('Decommissioned', 'Decommissioned'),
    ]
    
    # Relationship to CSV upload
    csv_upload = models.ForeignKey(
        CSVUpload, 
        on_delete=models.CASCADE, 
        related_name='equipment',
        null=True,
        blank=True
    )
    
    # Equipment identification
    equipment_id = models.CharField(max_length=100, unique=True)
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=50, choices=EQUIPMENT_TYPES)
    
    # Equipment specifications
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    model_number = models.CharField(max_length=100, blank=True, null=True)
    serial_number = models.CharField(max_length=100, blank=True, null=True)
    
    # Operational data
    capacity = models.FloatField(
        validators=[MinValueValidator(0.0)],
        help_text="Capacity in appropriate units",
        null=True,
        blank=True
    )
    flowrate = models.FloatField(
        validators=[MinValueValidator(0.0)],
        help_text="Flow rate in L/min or appropriate units",
        null=True,
        blank=True
    )
    pressure = models.FloatField(
        validators=[MinValueValidator(0.0)],
        help_text="Operating pressure in bar or psi",
        null=True,
        blank=True
    )
    temperature = models.FloatField(
        help_text="Operating temperature in °C",
        null=True,
        blank=True
    )
    
    # Location and status
    location = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    
    # Timestamps
    installation_date = models.DateField(null=True, blank=True)
    last_maintenance = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Additional notes
    notes = models.TextField(blank=True, null=True)
    
    # Dynamic parameters - store any additional columns from CSV as JSON
    additional_params = models.JSONField(
        default=dict,
        blank=True,
        help_text="Store additional dynamic parameters from CSV (e.g., humidity, vibration, etc.)"
    )
    
    class Meta:
        ordering = ['equipment_id']
        verbose_name = 'Equipment'
        verbose_name_plural = 'Equipment'
        indexes = [
            models.Index(fields=['equipment_id']),
            models.Index(fields=['equipment_type']),
            models.Index(fields=['status']),
        ]
    
    def __str__(self):
        return f"{self.equipment_id} - {self.equipment_name}"
    
    @property
    def is_operational(self):
        """Check if equipment is operational."""
        return self.status == 'Active'
    
    @property
    def needs_maintenance(self):
        """Check if equipment needs maintenance based on last maintenance date."""
        if not self.last_maintenance:
            return True
        days_since_maintenance = (timezone.now().date() - self.last_maintenance).days
        return days_since_maintenance > 180  # 6 months


class DataSummary(models.Model):
    """
    Model to store aggregated summary statistics for dashboard.
    """
    csv_upload = models.OneToOneField(
        CSVUpload,
        on_delete=models.CASCADE,
        related_name='summary'
    )
    
    # Summary statistics
    total_equipment = models.IntegerField(default=0)
    active_equipment = models.IntegerField(default=0)
    inactive_equipment = models.IntegerField(default=0)
    maintenance_equipment = models.IntegerField(default=0)
    
    # Type distribution
    type_distribution = models.JSONField(default=dict)
    
    # Operational statistics
    avg_flowrate = models.FloatField(null=True, blank=True)
    max_flowrate = models.FloatField(null=True, blank=True)
    min_flowrate = models.FloatField(null=True, blank=True)
    
    avg_pressure = models.FloatField(null=True, blank=True)
    avg_temperature = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Data Summary'
        verbose_name_plural = 'Data Summaries'
    
    def __str__(self):
        return f"Summary for {self.csv_upload.filename}"

