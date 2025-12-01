import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KITCHARY_final.settings')
django.setup()

from core.models import MenuItem, UserProfile
from django.contrib.auth.models import User

def create_sample_data():
    print("Creating sample data...")
    
    # Create menu items
    menu_items = [
        {'name': 'Margherita Pizza', 'description': 'Classic pizza with tomato sauce, mozzarella, and basil', 'price': 12.99},
        {'name': 'Chicken Biryani', 'description': 'Aromatic rice dish with tender chicken and spices', 'price': 15.99},
        {'name': 'Caesar Salad', 'description': 'Fresh romaine lettuce with caesar dressing and croutons', 'price': 8.99},
        {'name': 'Beef Burger', 'description': 'Juicy beef patty with lettuce, tomato, and cheese', 'price': 11.99},
        {'name': 'Pasta Carbonara', 'description': 'Creamy pasta with bacon, eggs, and parmesan cheese', 'price': 13.99},
        {'name': 'Fish and Chips', 'description': 'Crispy battered fish with golden french fries', 'price': 14.99},
    ]
    
    for item_data in menu_items:
        item, created = MenuItem.objects.get_or_create(
            name=item_data['name'],
            defaults={
                'description': item_data['description'],
                'price': item_data['price']
            }
        )
        if created:
            print(f"Created menu item: {item.name}")
        else:
            print(f"Menu item already exists: {item.name}")
    
    # Create admin user if doesn't exist
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@kitchary.com',
            password='admin123'
        )
        UserProfile.objects.create(user=admin_user, role='admin')
        print("Created admin user: admin/admin123")
    else:
        print("Admin user already exists")
    
    # Create test customer if doesn't exist
    if not User.objects.filter(username='customer').exists():
        customer_user = User.objects.create_user(
            username='customer',
            email='customer@test.com',
            password='customer123'
        )
        UserProfile.objects.create(user=customer_user, role='customer')
        print("Created customer user: customer/customer123")
    else:
        print("Customer user already exists")
    
    print("\nSample data creation completed!")
    print("You can now login with:")
    print("Admin: admin/admin123")
    print("Customer: customer/customer123")

if __name__ == '__main__':
    create_sample_data()
