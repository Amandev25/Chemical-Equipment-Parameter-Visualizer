"""
Serializers for API models and responses.
"""
from rest_framework import serializers
from .models import CSVUpload, Equipment, DataSummary


class EquipmentSerializer(serializers.ModelSerializer):
    """
    Serializer for Equipment model.
    Includes dynamic parameters from additional_params JSONField.
    """
    is_operational = serializers.ReadOnlyField()
    needs_maintenance = serializers.ReadOnlyField()
    
    class Meta:
        model = Equipment
        fields = [
            'id', 'equipment_id', 'equipment_name', 'equipment_type',
            'manufacturer', 'model_number', 'serial_number',
            'capacity', 'flowrate', 'pressure', 'temperature',
            'location', 'status', 'installation_date', 'last_maintenance',
            'notes', 'additional_params', 'is_operational', 'needs_maintenance',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def to_representation(self, instance):
        """
        Flatten additional_params into the main response for easier frontend access.
        """
        representation = super().to_representation(instance)
        additional_params = representation.pop('additional_params', {}) or {}
        # Merge additional_params into the main representation
        representation.update(additional_params)
        return representation


class EquipmentListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for equipment lists.
    Includes dynamic parameters from additional_params JSONField.
    """
    csv_upload_id = serializers.IntegerField(source='csv_upload.id', read_only=True)
    csv_upload_filename = serializers.CharField(source='csv_upload.filename', read_only=True)
    
    class Meta:
        model = Equipment
        fields = [
            'id', 'equipment_id', 'equipment_name', 'equipment_type',
            'flowrate', 'pressure', 'temperature', 'status', 'location',
            'csv_upload_id', 'csv_upload_filename', 'additional_params'
        ]
    
    def to_representation(self, instance):
        """
        Flatten additional_params into the main response for easier frontend access.
        """
        representation = super().to_representation(instance)
        additional_params = representation.pop('additional_params', {}) or {}
        # Merge additional_params into the main representation
        representation.update(additional_params)
        return representation


class CSVUploadSerializer(serializers.ModelSerializer):
    """
    Serializer for CSV upload tracking.
    """
    equipment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = CSVUpload
        fields = [
            'id', 'file', 'filename', 'uploaded_at',
            'processed', 'total_records', 'equipment_count'
        ]
        read_only_fields = ['id', 'uploaded_at', 'processed', 'total_records']
    
    def get_equipment_count(self, obj):
        return obj.equipment.count()


class DataSummarySerializer(serializers.ModelSerializer):
    """
    Serializer for data summary statistics.
    """
    upload_info = serializers.SerializerMethodField()
    
    class Meta:
        model = DataSummary
        fields = [
            'id', 'upload_info', 'total_equipment', 'active_equipment',
            'inactive_equipment', 'maintenance_equipment',
            'type_distribution', 'avg_flowrate', 'max_flowrate',
            'min_flowrate', 'avg_pressure', 'avg_temperature',
            'created_at', 'updated_at'
        ]
    
    def get_upload_info(self, obj):
        return {
            'filename': obj.csv_upload.filename,
            'uploaded_at': obj.csv_upload.uploaded_at
        }


class FileUploadSerializer(serializers.Serializer):
    """
    Serializer for file upload validation.
    """
    file = serializers.FileField()
    
    def validate_file(self, value):
        """
        Validate uploaded file.
        """
        # Check file extension
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed.")
        
        # Check file size (10MB limit)
        if value.size > 10 * 1024 * 1024:
            raise serializers.ValidationError("File size must not exceed 10MB.")
        
        return value


class ChartDataSerializer(serializers.Serializer):
    """
    Serializer for chart data responses.
    """
    labels = serializers.ListField(child=serializers.CharField())
    datasets = serializers.ListField(child=serializers.DictField())


class FlowrateChartSerializer(serializers.Serializer):
    """
    Serializer for flowrate chart data.
    """
    equipment_ids = serializers.ListField(child=serializers.CharField())
    flowrates = serializers.ListField(child=serializers.FloatField())


class TypeDistributionSerializer(serializers.Serializer):
    """
    Serializer for equipment type distribution.
    """
    types = serializers.ListField(child=serializers.CharField())
    counts = serializers.ListField(child=serializers.IntegerField())
    percentages = serializers.ListField(child=serializers.FloatField())


class SummaryCardsSerializer(serializers.Serializer):
    """
    Serializer for dashboard summary cards.
    """
    total_equipment = serializers.IntegerField()
    active_equipment = serializers.IntegerField()
    inactive_equipment = serializers.IntegerField()
    maintenance_equipment = serializers.IntegerField()
    avg_flowrate = serializers.FloatField(allow_null=True)
    avg_pressure = serializers.FloatField(allow_null=True)
    avg_temperature = serializers.FloatField(allow_null=True)
    total_types = serializers.IntegerField()


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.
    """
    class Meta:
        from django.contrib.auth.models import User
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class RegisterSerializer(serializers.Serializer):
    """
    Serializer for user registration.
    """
    username = serializers.CharField(max_length=150, required=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True, required=True, min_length=6)
    password_confirm = serializers.CharField(write_only=True, required=True, min_length=6)
    
    def validate_username(self, value):
        from django.contrib.auth.models import User
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with this username already exists.")
        return value
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords do not match.")
        return attrs
    
    def create(self, validated_data):
        from django.contrib.auth.models import User
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user

