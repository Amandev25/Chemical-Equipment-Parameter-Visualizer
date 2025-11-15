"""
API views for chemical equipment data management.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Q
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.decorators import method_decorator
from .models import Equipment, CSVUpload, DataSummary
from .serializers import (
    EquipmentSerializer, EquipmentListSerializer, CSVUploadSerializer,
    DataSummarySerializer, FileUploadSerializer, FlowrateChartSerializer,
    TypeDistributionSerializer, SummaryCardsSerializer, UserSerializer, RegisterSerializer
)
from .utils import (
    parse_csv_file, save_equipment_from_csv, calculate_summary_statistics,
    generate_equipment_pdf, get_flowrate_chart_data, get_type_distribution_data,
    get_dashboard_summary
)


class EquipmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Equipment CRUD operations.
    Filters equipment by authenticated user.
    """
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        """Return appropriate serializer based on action."""
        if self.action == 'list':
            return EquipmentListSerializer
        return EquipmentSerializer
    
    def get_queryset(self):
        """
        Filter queryset based on query parameters and user.
        """
        # Filter by user's CSV uploads
        user_csv_uploads = CSVUpload.objects.filter(user=self.request.user)
        queryset = Equipment.objects.filter(csv_upload__in=user_csv_uploads)
        
        # Filter by CSV upload
        csv_upload_id = self.request.query_params.get('csv_upload', None)
        if csv_upload_id:
            # Ensure the CSV upload belongs to the user
            if user_csv_uploads.filter(id=csv_upload_id).exists():
                queryset = queryset.filter(csv_upload_id=csv_upload_id)
            else:
                queryset = queryset.none()
        
        # Filter by equipment type
        equipment_type = self.request.query_params.get('type', None)
        if equipment_type:
            queryset = queryset.filter(equipment_type=equipment_type)
        
        # Filter by status
        equipment_status = self.request.query_params.get('status', None)
        if equipment_status:
            queryset = queryset.filter(status=equipment_status)
        
        # Search by name or ID
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(equipment_name__icontains=search) |
                Q(equipment_id__icontains=search)
            )
        
        return queryset.order_by('equipment_id')
    
    @action(detail=False, methods=['get'])
    def types(self, request):
        """Get list of unique equipment types for the authenticated user."""
        user_csv_uploads = CSVUpload.objects.filter(user=request.user)
        types = Equipment.objects.filter(csv_upload__in=user_csv_uploads).values_list('equipment_type', flat=True).distinct()
        return Response({'types': list(types)})
    
    @action(detail=False, methods=['get'])
    def statuses(self, request):
        """Get list of equipment statuses."""
        statuses = [choice[0] for choice in Equipment.STATUS_CHOICES]
        return Response({'statuses': statuses})


class CSVUploadViewSet(viewsets.ModelViewSet):
    """
    ViewSet for CSV upload management.
    Keeps only the last 5 CSV uploads per user.
    """
    queryset = CSVUpload.objects.all()
    serializer_class = CSVUploadSerializer
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Return only the last 5 CSV uploads for the authenticated user (most recent first).
        """
        return CSVUpload.objects.filter(user=self.request.user).order_by('-uploaded_at')[:5]
    
    def create(self, request, *args, **kwargs):
        """
        Handle CSV file upload and processing.
        """
        file_serializer = FileUploadSerializer(data=request.data)
        
        if not file_serializer.is_valid():
            return Response(
                file_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        uploaded_file = file_serializer.validated_data['file']
        
        # Create CSVUpload record associated with the user
        csv_upload = CSVUpload.objects.create(
            user=self.request.user,
            file=uploaded_file,
            filename=uploaded_file.name
        )
        
        # Parse CSV file
        success, data_list, error_msg = parse_csv_file(csv_upload.file.path)
        
        if not success:
            csv_upload.delete()
            return Response(
                {'error': error_msg},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Save equipment data
        created_count, updated_count = save_equipment_from_csv(csv_upload, data_list)
        
        # Calculate summary statistics
        summary = calculate_summary_statistics(csv_upload)
        
        # Update CSV upload record
        csv_upload.processed = True
        csv_upload.total_records = created_count + updated_count
        csv_upload.save()
        
        # Keep only the last 5 CSV uploads per user, delete older ones
        user_uploads = CSVUpload.objects.filter(user=self.request.user).order_by('-uploaded_at')
        total_count = user_uploads.count()
        if total_count > 5:
            # Get IDs of uploads to keep (first 5, which are the most recent)
            keep_ids = list(user_uploads[:5].values_list('id', flat=True))
            # Get all uploads that should be deleted (older than the 5th most recent)
            old_uploads = CSVUpload.objects.filter(user=self.request.user).exclude(id__in=keep_ids)
            
            # Delete associated data for each old upload
            for old_upload in old_uploads:
                # Delete associated equipment (CASCADE will handle it, but explicit for clarity)
                old_upload.equipment.all().delete()
                # Delete summary if it exists
                try:
                    old_upload.summary.delete()
                except DataSummary.DoesNotExist:
                    pass
                # Delete the file from storage
                if old_upload.file:
                    old_upload.file.delete(save=False)
                # Delete the CSV upload record
                old_upload.delete()
        
        return Response({
            'message': 'CSV file processed successfully',
            'csv_upload_id': csv_upload.id,
            'filename': csv_upload.filename,
            'created_count': created_count,
            'updated_count': updated_count,
            'total_records': csv_upload.total_records,
            'summary': DataSummarySerializer(summary).data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['get'])
    def equipment(self, request, pk=None):
        """Get all equipment from a specific CSV upload."""
        csv_upload = self.get_object()
        # Ensure the CSV upload belongs to the user
        if csv_upload.user != request.user:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        equipment = csv_upload.equipment.all()
        serializer = EquipmentListSerializer(equipment, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        """Get summary statistics for a specific CSV upload."""
        csv_upload = self.get_object()
        # Ensure the CSV upload belongs to the user
        if csv_upload.user != request.user:
            return Response(
                {'error': 'Not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        try:
            summary = csv_upload.summary
            serializer = DataSummarySerializer(summary)
            return Response(serializer.data)
        except DataSummary.DoesNotExist:
            return Response(
                {'error': 'Summary not found'},
                status=status.HTTP_404_NOT_FOUND
            )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_summary(request):
    """
    Get summary statistics for dashboard cards.
    """
    summary_data = get_dashboard_summary(user=request.user)
    serializer = SummaryCardsSerializer(data=summary_data)
    serializer.is_valid()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def flowrate_chart_data(request):
    """
    Get data for flowrate chart visualization.
    """
    csv_upload_id = request.query_params.get('csv_upload', None)
    csv_upload_id = int(csv_upload_id) if csv_upload_id else None
    chart_data = get_flowrate_chart_data(csv_upload_id=csv_upload_id, user=request.user)
    serializer = FlowrateChartSerializer(data=chart_data)
    serializer.is_valid()
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def type_distribution_data(request):
    """
    Get data for equipment type distribution chart.
    """
    csv_upload_id = request.query_params.get('csv_upload', None)
    csv_upload_id = int(csv_upload_id) if csv_upload_id else None
    distribution_data = get_type_distribution_data(csv_upload_id=csv_upload_id, user=request.user)
    serializer = TypeDistributionSerializer(data=distribution_data)
    serializer.is_valid()
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def generate_report(request):
    """
    Generate PDF report for equipment data.
    """
    # Get filter parameters
    equipment_type = request.data.get('type', None)
    equipment_status = request.data.get('status', None)
    
    # Build queryset - filter by user's CSV uploads
    user_csv_uploads = CSVUpload.objects.filter(user=request.user)
    queryset = Equipment.objects.filter(csv_upload__in=user_csv_uploads)
    
    if equipment_type:
        queryset = queryset.filter(equipment_type=equipment_type)
    
    if equipment_status:
        queryset = queryset.filter(status=equipment_status)
    
    equipment_list = list(queryset)
    
    # Get summary data
    summary_data = get_dashboard_summary(user=request.user)
    
    # Generate PDF
    pdf_buffer = generate_equipment_pdf(equipment_list, summary_data)
    
    # Create HTTP response with PDF
    response = HttpResponse(pdf_buffer.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="equipment_report_{request.data.get("filename", "report")}.pdf"'
    
    return response


@api_view(['DELETE'])
def clear_all_data(request):
    """
    Clear all equipment and CSV upload data (for testing/development).
    """
    equipment_count = Equipment.objects.count()
    csv_count = CSVUpload.objects.count()
    
    Equipment.objects.all().delete()
    CSVUpload.objects.all().delete()
    DataSummary.objects.all().delete()
    
    return Response({
        'message': 'All data cleared successfully',
        'equipment_deleted': equipment_count,
        'csv_uploads_deleted': csv_count
    })


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    """
    API health check endpoint.
    """
    return Response({
        'status': 'healthy',
        'message': 'Chemical Equipment Visualizer API is running',
        'version': '1.0.0',
    })


# Authentication endpoints
@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login_view(request):
    """
    User login endpoint.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        serializer = UserSerializer(user)
        return Response({
            'message': 'Login successful',
            'user': serializer.data
        })
    else:
        return Response(
            {'error': 'Invalid username or password'},
            status=status.HTTP_401_UNAUTHORIZED
        )


@api_view(['POST'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def register_view(request):
    """
    User registration endpoint.
    """
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        login(request, user)
        user_serializer = UserSerializer(user)
        return Response({
            'message': 'Registration successful',
            'user': user_serializer.data
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    User logout endpoint.
    """
    logout(request)
    return Response({'message': 'Logout successful'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Get current authenticated user information.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def get_csrf_token(request):
    """
    Get CSRF token for authenticated requests.
    """
    token = get_token(request)
    return Response({'csrfToken': token})

