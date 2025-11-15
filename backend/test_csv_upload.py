"""
Test script to verify CSV parsing with the provided format.
Run this before uploading to the API.
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.utils import parse_csv_file

def test_csv_parsing():
    """Test CSV parsing with the sample file."""
    
    # Test with user's CSV file
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'sample_equipment_data.csv')
    
    if not os.path.exists(csv_path):
        print(f"[ERROR] CSV file not found at: {csv_path}")
        return False
    
    print("=" * 60)
    print("Testing CSV Upload with your file format")
    print("=" * 60)
    print(f"\nFile: {csv_path}\n")
    
    # Parse the CSV
    success, data_list, error_msg = parse_csv_file(csv_path)
    
    if not success:
        print(f"[ERROR] {error_msg}")
        return False
    
    print(f"[SUCCESS] Successfully parsed CSV file!")
    print(f"Total records found: {len(data_list)}\n")
    
    # Display first few records
    print("Sample Records:")
    print("-" * 60)
    
    for i, data in enumerate(data_list[:5], 1):
        print(f"\n{i}. Equipment ID: {data.get('equipment_id')}")
        print(f"   Name: {data.get('equipment_name')}")
        print(f"   Type: {data.get('equipment_type')}")
        print(f"   Flowrate: {data.get('flowrate')}")
        print(f"   Pressure: {data.get('pressure')}")
        print(f"   Temperature: {data.get('temperature')}")
    
    if len(data_list) > 5:
        print(f"\n   ... and {len(data_list) - 5} more records")
    
    print("\n" + "=" * 60)
    print("[SUCCESS] CSV Format Validation PASSED!")
    print("=" * 60)
    print("\nYour CSV file is ready to be uploaded to the API!")
    print("\nNext steps:")
    print("1. Start the server: python manage.py runserver")
    print("2. Go to: http://localhost:8000/swagger/")
    print("3. Upload your CSV using /api/uploads/ endpoint")
    
    return True

if __name__ == '__main__':
    try:
        test_csv_parsing()
    except Exception as e:
        print(f"\n[ERROR] {str(e)}")
        import traceback
        traceback.print_exc()

