import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KITCHARY_final.settings')
django.setup()

from core.models import MenuItem, User, UserProfile
from django.db.models import Count

print("Cleaning duplicate menu items...")

# Find duplicates
duplicates = MenuItem.objects.values('name').annotate(name_count=Count('name')).filter(name_count__gt=1)

for dup in duplicates:
    name = dup['name']
    items = MenuItem.objects.filter(name=name)
    print(f"Found {items.count()} items named '{name}'")
    
    # Keep the first item, delete the rest
    first_item = items.first()
    items.exclude(id=first_item.id).delete()
    print(f"Kept one '{name}' item, deleted {dup['name_count']-1} duplicates")

print("\nCleaning completed!")

# Create admin user if needed
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser(
        username='admin',
        email='admin@kitchary.com',
        password='admin123'
    )
    UserProfile.objects.create(user=admin_user, role='admin')
    print("Created admin user: admin/admin123")

print("\nFinal menu items:")
for item in MenuItem.objects.all():
    print(f"- {item.name}: ${item.price}")
