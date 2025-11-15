"""
Admin configuration for API models.
"""
from django.contrib import admin
from .models import CSVUpload, Equipment, DataSummary


@admin.register(CSVUpload)
class CSVUploadAdmin(admin.ModelAdmin):
    list_display = ['filename', 'uploaded_at', 'processed', 'total_records']
    list_filter = ['processed', 'uploaded_at']
    search_fields = ['filename']
    readonly_fields = ['uploaded_at']


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = [
        'equipment_id', 'equipment_name', 'equipment_type',
        'status', 'flowrate', 'location', 'created_at'
    ]
    list_filter = ['equipment_type', 'status', 'manufacturer']
    search_fields = ['equipment_id', 'equipment_name', 'serial_number']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Identification', {
            'fields': ('equipment_id', 'equipment_name', 'equipment_type')
        }),
        ('Specifications', {
            'fields': ('manufacturer', 'model_number', 'serial_number')
        }),
        ('Operational Data', {
            'fields': ('capacity', 'flowrate', 'pressure', 'temperature')
        }),
        ('Location & Status', {
            'fields': ('location', 'status')
        }),
        ('Dates', {
            'fields': ('installation_date', 'last_maintenance', 'created_at', 'updated_at')
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )


@admin.register(DataSummary)
class DataSummaryAdmin(admin.ModelAdmin):
    list_display = [
        'csv_upload', 'total_equipment', 'active_equipment',
        'avg_flowrate', 'created_at'
    ]
    readonly_fields = ['created_at', 'updated_at']

