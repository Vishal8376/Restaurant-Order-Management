import os
import django
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KITCHARY_final.settings')
django.setup()

from core.models import MenuItem, User, UserProfile

print("Existing Menu Items:")
for item in MenuItem.objects.all():
    print(f"- {item.name}: ${item.price}")

print(f"\nTotal menu items: {MenuItem.objects.count()}")

print("\nExisting Users:")
for user in User.objects.all():
    try:
        profile = user.userprofile
        print(f"- {user.username} ({profile.role})")
    except:
        print(f"- {user.username} (no profile)")
