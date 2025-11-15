"""
Utility functions for CSV parsing, PDF generation, and data processing.
"""
import pandas as pd
import csv
from datetime import datetime
from io import BytesIO
from typing import List, Dict, Any
from django.db.models import Avg, Max, Min, Count, Q
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph,
    Spacer, PageBreak, Image
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from .models import Equipment, CSVUpload, DataSummary


def parse_csv_file(file_path: str) -> tuple[bool, List[Dict[str, Any]], str]:
    """
    Parse CSV file and return equipment data.
    
    Args:
        file_path: Path to the CSV file
    
    Returns:
        Tuple of (success, data_list, error_message)
    """
    try:
        # Read CSV file using pandas
        df = pd.read_csv(file_path)
        
        # Store original column names for better error messages
        original_columns = df.columns.tolist()
        
        # Convert column names to lowercase and replace spaces with underscores
        df.columns = df.columns.str.lower().str.replace(' ', '_').str.strip()
        
        # Expected columns (flexible mapping)
        column_mapping = {
            'equipment_id': ['equipment_id', 'id', 'equip_id', 'equipment_no', 'equipment_name'],
            'equipment_name': ['equipment_name', 'name', 'equip_name', 'equipment_name'],
            'equipment_type': ['equipment_type', 'type', 'equip_type'],
            'manufacturer': ['manufacturer', 'make', 'vendor'],
            'model_number': ['model_number', 'model', 'model_no'],
            'serial_number': ['serial_number', 'serial', 'serial_no'],
            'capacity': ['capacity', 'cap'],
            'flowrate': ['flowrate', 'flow_rate', 'flow'],
            'pressure': ['pressure', 'press'],
            'temperature': ['temperature', 'temp'],
            'location': ['location', 'loc', 'site'],
            'status': ['status', 'state'],
            'installation_date': ['installation_date', 'install_date', 'commissioned_date'],
            'last_maintenance': ['last_maintenance', 'last_maint', 'maintenance_date'],
            'notes': ['notes', 'remarks', 'comments'],
        }
        
        # Map columns
        mapped_columns = {}
        for target_col, possible_names in column_mapping.items():
            for name in possible_names:
                if name in df.columns:
                    mapped_columns[name] = target_col
                    break
        
        # Rename columns
        df.rename(columns=mapped_columns, inplace=True)
        
        # Handle case where Equipment Name is used for both ID and Name
        if 'equipment_name' in df.columns and 'equipment_id' not in df.columns:
            df['equipment_id'] = df['equipment_name']
        elif 'equipment_id' in df.columns and 'equipment_name' not in df.columns:
            df['equipment_name'] = df['equipment_id']
        
        # Ensure required columns exist (only Equipment Name/ID and Type are required)
        # Check if we have at least one identifier column
        has_id = 'equipment_id' in df.columns or 'equipment_name' in df.columns
        has_type = 'equipment_type' in df.columns
        
        if not has_id:
            available_cols = ', '.join(original_columns)
            return False, [], f"Missing required column: Equipment Name or Equipment ID. Available columns: {available_cols}"
        
        if not has_type:
            available_cols = ', '.join(original_columns)
            return False, [], f"Missing required column: Equipment Type. Available columns: {available_cols}"
        
        # Convert dates first
        date_columns = ['installation_date', 'last_maintenance']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Known numeric columns (will be stored in model fields)
        known_numeric_columns = ['capacity', 'flowrate', 'pressure', 'temperature']
        for col in known_numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Known standard columns that will be stored in model fields
        standard_columns = [
            'equipment_id', 'equipment_name', 'equipment_type',
            'manufacturer', 'model_number', 'serial_number',
            'capacity', 'flowrate', 'pressure', 'temperature',
            'location', 'status', 'installation_date', 'last_maintenance', 'notes'
        ]
        
        # Handle missing values - replace NaN with None for proper JSON serialization
        df = df.where(pd.notnull(df), None)
        
        # For non-numeric, non-date standard columns, replace None with empty string
        for col in df.columns:
            if col not in known_numeric_columns and col not in date_columns and col in standard_columns:
                df[col] = df[col].fillna('')
        
        # Convert to list of dictionaries
        data_list = df.to_dict('records')
        
        # Separate standard columns from dynamic columns for each record
        processed_data = []
        for record in data_list:
            standard_data = {}
            dynamic_data = {}
            
            for key, value in record.items():
                if key in standard_columns:
                    standard_data[key] = value
                else:
                    # Store dynamic columns
                    # Try to convert to numeric if possible
                    if value is not None and value != '':
                        try:
                            # Try to convert to float
                            numeric_value = pd.to_numeric(value, errors='coerce')
                            if pd.notna(numeric_value):
                                dynamic_data[key] = float(numeric_value)
                            else:
                                dynamic_data[key] = str(value) if value else None
                        except (ValueError, TypeError):
                            dynamic_data[key] = str(value) if value else None
                    else:
                        dynamic_data[key] = None
            
            # Combine standard and dynamic data
            processed_record = {**standard_data, 'additional_params': dynamic_data}
            processed_data.append(processed_record)
        
        return True, processed_data, ""
    
    except Exception as e:
        return False, [], f"Error parsing CSV file: {str(e)}"


def save_equipment_from_csv(csv_upload: CSVUpload, data_list: List[Dict[str, Any]]) -> tuple[int, int]:
    """
    Save equipment data from parsed CSV to database.
    
    Args:
        csv_upload: CSVUpload instance
        data_list: List of equipment data dictionaries
    
    Returns:
        Tuple of (created_count, updated_count)
    """
    created_count = 0
    updated_count = 0
    
    for data in data_list:
        equipment_id = data.get('equipment_id', '').strip()
        if not equipment_id:
            continue
        
        # Get equipment name, use equipment_id if name is empty
        equip_name = data.get('equipment_name', '') or data.get('equipment_id', '')
        equip_type = data.get('equipment_type', 'Other')
        
        # Clean up equipment type (remove spaces, handle variations)
        if equip_type:
            equip_type = equip_type.strip()
            # Map common variations to standard types
            type_mapping = {
                'heatexchanger': 'Heat Exchanger',
                'heat_exchanger': 'Heat Exchanger',
                'condenser': 'Heat Exchanger',  # Condenser is a type of heat exchanger
            }
            equip_type_lower = equip_type.lower().replace(' ', '')
            equip_type = type_mapping.get(equip_type_lower, equip_type)
        
        # Helper function to convert NaN/None to None for numeric fields
        def clean_numeric_value(value):
            """Convert NaN, None, or empty string to None for numeric fields."""
            import math
            if value is None or value == '':
                return None
            # Check for NaN (float('nan') or numpy NaN)
            if isinstance(value, float) and math.isnan(value):
                return None
            return value
        
        # Get additional dynamic parameters
        additional_params = data.get('additional_params', {}) or {}
        
        # Prepare equipment data
        equipment_data = {
            'equipment_name': equip_name,
            'equipment_type': equip_type,
            'manufacturer': data.get('manufacturer', None) or None,
            'model_number': data.get('model_number', None) or None,
            'serial_number': data.get('serial_number', None) or None,
            'capacity': clean_numeric_value(data.get('capacity', None)),
            'flowrate': clean_numeric_value(data.get('flowrate', None)),
            'pressure': clean_numeric_value(data.get('pressure', None)),
            'temperature': clean_numeric_value(data.get('temperature', None)),
            'location': data.get('location', None) or None,
            'status': data.get('status', 'Active'),
            'installation_date': data.get('installation_date', None),
            'last_maintenance': data.get('last_maintenance', None),
            'notes': data.get('notes', None) or None,
            'additional_params': additional_params,
            'csv_upload': csv_upload,
        }
        
        # Create or update equipment
        equipment, created = Equipment.objects.update_or_create(
            equipment_id=equipment_id,
            defaults=equipment_data
        )
        
        if created:
            created_count += 1
        else:
            updated_count += 1
    
    return created_count, updated_count


def calculate_summary_statistics(csv_upload: CSVUpload) -> DataSummary:
    """
    Calculate and save summary statistics for uploaded data.
    
    Args:
        csv_upload: CSVUpload instance
    
    Returns:
        DataSummary instance
    """
    equipment_qs = Equipment.objects.filter(csv_upload=csv_upload)
    
    # Count by status
    total_equipment = equipment_qs.count()
    active_equipment = equipment_qs.filter(status='Active').count()
    inactive_equipment = equipment_qs.filter(status='Inactive').count()
    maintenance_equipment = equipment_qs.filter(status='Maintenance').count()
    
    # Type distribution
    type_dist = equipment_qs.values('equipment_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    type_distribution = {item['equipment_type']: item['count'] for item in type_dist}
    
    # Operational statistics
    flow_stats = equipment_qs.aggregate(
        avg_flowrate=Avg('flowrate'),
        max_flowrate=Max('flowrate'),
        min_flowrate=Min('flowrate')
    )
    
    pressure_stats = equipment_qs.aggregate(avg_pressure=Avg('pressure'))
    temp_stats = equipment_qs.aggregate(avg_temperature=Avg('temperature'))
    
    # Create or update summary
    summary, created = DataSummary.objects.update_or_create(
        csv_upload=csv_upload,
        defaults={
            'total_equipment': total_equipment,
            'active_equipment': active_equipment,
            'inactive_equipment': inactive_equipment,
            'maintenance_equipment': maintenance_equipment,
            'type_distribution': type_distribution,
            'avg_flowrate': flow_stats['avg_flowrate'],
            'max_flowrate': flow_stats['max_flowrate'],
            'min_flowrate': flow_stats['min_flowrate'],
            'avg_pressure': pressure_stats['avg_pressure'],
            'avg_temperature': temp_stats['avg_temperature'],
        }
    )
    
    return summary


def generate_equipment_pdf(equipment_list: List[Equipment] = None, summary_data: Dict = None) -> BytesIO:
    """
    Generate PDF report for equipment data.
    
    Args:
        equipment_list: List of Equipment objects to include in report
        summary_data: Optional summary statistics dictionary
    
    Returns:
        BytesIO buffer containing PDF data
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a5490'),
        alignment=TA_CENTER,
        spaceAfter=30
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=12
    )
    
    # Title
    story.append(Paragraph("Chemical Equipment Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Report metadata
    report_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    story.append(Paragraph(f"Generated: {report_date}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Summary section
    if summary_data:
        story.append(Paragraph("Summary Statistics", heading_style))
        
        summary_table_data = [
            ['Metric', 'Value'],
            ['Total Equipment', str(summary_data.get('total_equipment', 0))],
            ['Active Equipment', str(summary_data.get('active_equipment', 0))],
            ['Inactive Equipment', str(summary_data.get('inactive_equipment', 0))],
            ['Maintenance Required', str(summary_data.get('maintenance_equipment', 0))],
        ]
        
        if summary_data.get('avg_flowrate'):
            summary_table_data.append(['Average Flow Rate', f"{summary_data['avg_flowrate']:.2f} L/min"])
        
        summary_table = Table(summary_table_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        
        story.append(summary_table)
        story.append(Spacer(1, 0.3*inch))
    
    # Equipment details
    if equipment_list:
        story.append(Paragraph("Equipment Details", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Equipment table
        table_data = [['ID', 'Name', 'Type', 'Flow Rate', 'Status', 'Location']]
        
        for equipment in equipment_list[:50]:  # Limit to first 50 for PDF
            table_data.append([
                equipment.equipment_id[:15],  # Truncate long IDs
                equipment.equipment_name[:25],
                equipment.equipment_type,
                f"{equipment.flowrate:.1f}" if equipment.flowrate else 'N/A',
                equipment.status,
                (equipment.location[:15] if equipment.location else 'N/A'),
            ])
        
        equipment_table = Table(table_data, colWidths=[1*inch, 1.8*inch, 1.2*inch, 0.9*inch, 1*inch, 1*inch])
        equipment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.lightgrey]),
        ]))
        
        story.append(equipment_table)
        
        if len(equipment_list) > 50:
            story.append(Spacer(1, 0.2*inch))
            story.append(Paragraph(
                f"Note: Showing first 50 of {len(equipment_list)} equipment items.",
                styles['Italic']
            ))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer


def get_flowrate_chart_data(csv_upload_id: int = None, user=None) -> Dict[str, List]:
    """
    Get data for flowrate chart visualization.
    
    Args:
        csv_upload_id: Optional CSV upload ID to filter by
        user: User instance to filter by
    
    Returns:
        Dictionary with equipment_ids and flowrates
    """
    # Filter by user's CSV uploads
    if user:
        user_csv_uploads = CSVUpload.objects.filter(user=user)
        queryset = Equipment.objects.filter(
            csv_upload__in=user_csv_uploads,
            flowrate__isnull=False,
            status='Active'
        )
    else:
        queryset = Equipment.objects.filter(
            flowrate__isnull=False,
            status='Active'
        )
    
    if csv_upload_id:
        queryset = queryset.filter(csv_upload_id=csv_upload_id)
    
    equipment = queryset.order_by('-flowrate')[:20]
    
    return {
        'equipment_ids': [e.equipment_id for e in equipment],
        'flowrates': [float(e.flowrate) for e in equipment]
    }


def get_type_distribution_data(csv_upload_id: int = None, user=None) -> Dict[str, List]:
    """
    Get data for equipment type distribution chart.
    
    Args:
        csv_upload_id: Optional CSV upload ID to filter by
        user: User instance to filter by
    
    Returns:
        Dictionary with types, counts, and percentages
    """
    # Filter by user's CSV uploads
    if user:
        user_csv_uploads = CSVUpload.objects.filter(user=user)
        queryset = Equipment.objects.filter(csv_upload__in=user_csv_uploads)
    else:
        queryset = Equipment.objects.all()
    
    if csv_upload_id:
        queryset = queryset.filter(csv_upload_id=csv_upload_id)
    
    type_data = queryset.values('equipment_type').annotate(
        count=Count('id')
    ).order_by('-count')
    
    total = sum(item['count'] for item in type_data)
    
    types = [item['equipment_type'] for item in type_data]
    counts = [item['count'] for item in type_data]
    percentages = [round((item['count'] / total * 100), 2) if total > 0 else 0 for item in type_data]
    
    return {
        'types': types,
        'counts': counts,
        'percentages': percentages
    }


def get_dashboard_summary(user=None) -> Dict[str, Any]:
    """
    Get summary data for dashboard cards.
    
    Args:
        user: User instance to filter by
    
    Returns:
        Dictionary with summary statistics
    """
    # Filter by user's CSV uploads
    if user:
        user_csv_uploads = CSVUpload.objects.filter(user=user)
        equipment_queryset = Equipment.objects.filter(csv_upload__in=user_csv_uploads)
    else:
        equipment_queryset = Equipment.objects.all()
    
    total_equipment = equipment_queryset.count()
    active_equipment = equipment_queryset.filter(status='Active').count()
    inactive_equipment = equipment_queryset.filter(status='Inactive').count()
    maintenance_equipment = equipment_queryset.filter(status='Maintenance').count()
    
    stats = equipment_queryset.aggregate(
        avg_flowrate=Avg('flowrate'),
        avg_pressure=Avg('pressure'),
        avg_temperature=Avg('temperature')
    )
    
    total_types = equipment_queryset.values('equipment_type').distinct().count()
    
    return {
        'total_equipment': total_equipment,
        'active_equipment': active_equipment,
        'inactive_equipment': inactive_equipment,
        'maintenance_equipment': maintenance_equipment,
        'avg_flowrate': round(stats['avg_flowrate'], 2) if stats['avg_flowrate'] else None,
        'avg_pressure': round(stats['avg_pressure'], 2) if stats['avg_pressure'] else None,
        'avg_temperature': round(stats['avg_temperature'], 2) if stats['avg_temperature'] else None,
        'total_types': total_types
    }

