"""
API client for desktop application to communicate with Django backend.
"""
import requests
from typing import Optional, Dict, List, Any
import json


class APIClient:
    """Client for interacting with the Chemical Equipment Visualizer API."""
    
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.csrf_token: Optional[str] = None
        self.is_authenticated = False
        # Set Accept header for JSON responses
        self.session.headers.update({
            'Accept': 'application/json'
        })
        
    def _get_csrf_token(self) -> None:
        """Get CSRF token from the server."""
        try:
            # First get CSRF token from cookie by making a GET request
            response = self.session.get(f"{self.base_url}/auth/csrf/")
            if response.status_code == 200:
                data = response.json()
                self.csrf_token = data.get('csrfToken')
                # Also try to get CSRF token from cookie if available
                csrf_cookie = self.session.cookies.get('csrftoken')
                if csrf_cookie:
                    self.csrf_token = csrf_cookie
                if self.csrf_token:
                    self.session.headers.update({'X-CSRFToken': self.csrf_token})
        except Exception as e:
            print(f"Error getting CSRF token: {e}")
    
    def login(self, username: str, password: str) -> Dict[str, Any]:
        """Login user and establish session."""
        try:
            self._get_csrf_token()
            # Ensure we include CSRF token in headers
            headers = {
                'Content-Type': 'application/json'
            }
            if self.csrf_token:
                headers['X-CSRFToken'] = self.csrf_token
            
            response = self.session.post(
                f"{self.base_url}/auth/login/",
                json={'username': username, 'password': password},
                headers=headers
            )
            if response.status_code == 200:
                self.is_authenticated = True
                # Update CSRF token from response cookies if available
                csrf_cookie = self.session.cookies.get('csrftoken')
                if csrf_cookie:
                    self.csrf_token = csrf_cookie
                    self.session.headers.update({'X-CSRFToken': self.csrf_token})
                return {'success': True, 'data': response.json()}
            else:
                return {'success': False, 'error': response.json().get('error', 'Login failed')}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def register(self, username: str, password: str, password_confirm: str, email: str = '') -> Dict[str, Any]:
        """Register a new user."""
        try:
            self._get_csrf_token()
            headers = {
                'Content-Type': 'application/json'
            }
            if self.csrf_token:
                headers['X-CSRFToken'] = self.csrf_token
            
            response = self.session.post(
                f"{self.base_url}/auth/register/",
                json={
                    'username': username,
                    'password': password,
                    'password_confirm': password_confirm,
                    'email': email
                },
                headers=headers
            )
            if response.status_code == 201:
                self.is_authenticated = True
                return {'success': True, 'data': response.json()}
            else:
                return {'success': False, 'error': response.json()}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def logout(self) -> Dict[str, Any]:
        """Logout current user."""
        try:
            headers = {
                'Content-Type': 'application/json'
            }
            if self.csrf_token:
                headers['X-CSRFToken'] = self.csrf_token
            
            response = self.session.post(
                f"{self.base_url}/auth/logout/",
                headers=headers
            )
            self.is_authenticated = False
            return {'success': True}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_current_user(self) -> Dict[str, Any]:
        """Get current authenticated user."""
        try:
            headers = {}
            if self.csrf_token:
                headers['X-CSRFToken'] = self.csrf_token
            
            response = self.session.get(
                f"{self.base_url}/auth/me/",
                headers=headers
            )
            if response.status_code == 200:
                return {'success': True, 'data': response.json()}
            else:
                self.is_authenticated = False
                return {'success': False, 'error': 'Not authenticated'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Get dashboard summary statistics."""
        try:
            # Ensure CSRF token is in headers
            headers = {}
            if self.csrf_token:
                headers['X-CSRFToken'] = self.csrf_token
            
            response = self.session.get(
                f"{self.base_url}/dashboard/summary/",
                headers=headers
            )
            if response.status_code == 200:
                return {'success': True, 'data': response.json()}
            else:
                return {'success': False, 'error': response.json()}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_flowrate_chart_data(self, csv_upload_id: Optional[int] = None) -> Dict[str, Any]:
        """Get flowrate chart data."""
        try:
            params = {}
            if csv_upload_id:
                params['csv_upload'] = csv_upload_id
            
            headers = {}
            if self.csrf_token:
                headers['X-CSRFToken'] = self.csrf_token
            
            response = self.session.get(
                f"{self.base_url}/dashboard/flowrate-chart/",
                params=params,
                headers=headers
            )
            if response.status_code == 200:
                return {'success': True, 'data': response.json()}
            else:
                return {'success': False, 'error': response.json()}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_type_distribution_data(self, csv_upload_id: Optional[int] = None) -> Dict[str, Any]:
        """Get equipment type distribution data."""
        try:
            params = {}
            if csv_upload_id:
                params['csv_upload'] = csv_upload_id
            
            headers = {}
            if self.csrf_token:
                headers['X-CSRFToken'] = self.csrf_token
            
            response = self.session.get(
                f"{self.base_url}/dashboard/type-distribution/",
                params=params,
                headers=headers
            )
            if response.status_code == 200:
                return {'success': True, 'data': response.json()}
            else:
                return {'success': False, 'error': response.json()}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def upload_csv(self, file_path: str) -> Dict[str, Any]:
        """Upload CSV file."""
        try:
            self._get_csrf_token()
            # Don't set Content-Type for file uploads - requests will set multipart/form-data automatically
            headers = {}
            if self.csrf_token:
                headers['X-CSRFToken'] = self.csrf_token
            
            with open(file_path, 'rb') as f:
                files = {'file': (file_path.split('/')[-1], f, 'text/csv')}
                response = self.session.post(
                    f"{self.base_url}/uploads/",
                    files=files,
                    headers=headers
                )
            
            if response.status_code == 201:
                return {'success': True, 'data': response.json()}
            else:
                return {'success': False, 'error': response.json()}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_equipment(self, csv_upload_id: Optional[int] = None, equipment_type: Optional[str] = None) -> Dict[str, Any]:
        """Get equipment list."""
        try:
            params = {}
            if csv_upload_id:
                params['csv_upload'] = csv_upload_id
            if equipment_type:
                params['type'] = equipment_type
            
            headers = {}
            if self.csrf_token:
                headers['X-CSRFToken'] = self.csrf_token
            
            response = self.session.get(
                f"{self.base_url}/equipment/",
                params=params,
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                # Handle paginated or non-paginated responses
                if 'results' in data:
                    return {'success': True, 'data': data['results']}
                elif isinstance(data, list):
                    return {'success': True, 'data': data}
                else:
                    return {'success': True, 'data': data}
            else:
                return {'success': False, 'error': response.json()}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_equipment_types(self) -> Dict[str, Any]:
        """Get list of equipment types."""
        try:
            headers = {}
            if self.csrf_token:
                headers['X-CSRFToken'] = self.csrf_token
            
            response = self.session.get(
                f"{self.base_url}/equipment/types/",
                headers=headers
            )
            if response.status_code == 200:
                return {'success': True, 'data': response.json()}
            else:
                return {'success': False, 'error': response.json()}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def get_csv_uploads(self) -> Dict[str, Any]:
        """Get list of CSV uploads."""
        try:
            headers = {}
            if self.csrf_token:
                headers['X-CSRFToken'] = self.csrf_token
            
            response = self.session.get(
                f"{self.base_url}/uploads/",
                headers=headers
            )
            if response.status_code == 200:
                data = response.json()
                if 'results' in data:
                    return {'success': True, 'data': data['results']}
                elif isinstance(data, list):
                    return {'success': True, 'data': data}
                else:
                    return {'success': True, 'data': data}
            else:
                return {'success': False, 'error': response.json()}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def generate_report(self, equipment_type: Optional[str] = None) -> Dict[str, Any]:
        """Generate PDF report."""
        try:
            params = {}
            if equipment_type:
                params['type'] = equipment_type
            
            headers = {
                'Content-Type': 'application/json'
            }
            if self.csrf_token:
                headers['X-CSRFToken'] = self.csrf_token
            
            response = self.session.post(
                f"{self.base_url}/reports/generate/",
                json=params,
                headers=headers,
                stream=True
            )
            if response.status_code == 200:
                return {'success': True, 'data': response.content}
            else:
                return {'success': False, 'error': response.json()}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health."""
        try:
            response = self.session.get(f"{self.base_url}/health/")
            if response.status_code == 200:
                return {'success': True, 'data': response.json()}
            else:
                return {'success': False, 'error': 'API not healthy'}
        except Exception as e:
            return {'success': False, 'error': str(e)}


