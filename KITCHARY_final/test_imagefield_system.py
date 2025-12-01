#!/usr/bin/env python3
"""
Test the updated ImageField system for KITCHARY restaurant
Verifies that all menu items have proper images via ImageField
"""

import os
import sys
import django
from pathlib import Path

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KITCHARY_final.settings')
django.setup()

from core.models import MenuItem
from django.conf import settings

def test_imagefield_system():
    """Test the ImageField implementation"""
    print("=== TESTING IMAGEFIELD SYSTEM ===\n")
    
    # 1. Check media directory setup
    print("1. Media Directory Setup:")
    media_root = Path(settings.MEDIA_ROOT)
    media_images_dir = media_root / 'menu_images'
    
    print(f"   MEDIA_ROOT: {media_root}")
    print(f"   MEDIA_URL: {settings.MEDIA_URL}")
    print(f"   Media images directory: {media_images_dir}")
    print(f"   Directory exists: {media_images_dir.exists()}")
    
    if media_images_dir.exists():
        image_files = list(media_images_dir.glob('*.jpg'))
        print(f"   Image files found: {len(image_files)}")
        if image_files:
            print(f"   Sample files: {[f.name for f in image_files[:3]]}")
    
    print()
    
    # 2. Test menu items with ImageField
    print("2. Menu Items ImageField Test:")
    menu_items = MenuItem.objects.all()
    print(f"   Total menu items: {len(menu_items)}")
    
    items_with_images = 0
    items_without_images = 0
    
    for item in menu_items:
        print(f"\n   Item: {item.name}")
        
        # Test ImageField
        has_image = item.has_image()
        print(f"     Has ImageField: {has_image}")
        
        if has_image:
            print(f"     Image URL: {item.image.url}")
            print(f"     Image path: {item.image.path if hasattr(item.image, 'path') else 'N/A'}")
            
            # Check if file exists
            try:
                file_exists = os.path.exists(item.image.path)
                print(f"     File exists: {file_exists}")
                if file_exists:
                    file_size = os.path.getsize(item.image.path)
                    print(f"     File size: {file_size} bytes")
                    items_with_images += 1
                else:
                    items_without_images += 1
            except:
                print(f"     File check failed")
                items_without_images += 1
        else:
            items_without_images += 1
        
        # Test URL methods
        print(f"     get_image_url(): {item.get_image_url()}")
        print(f"     get_fallback_image_url(): {item.get_fallback_image_url()}")
        print(f"     get_image_alt_text(): {item.get_image_alt_text()}")
    
    print(f"\n=== SUMMARY ===")
    print(f"   Items with working images: {items_with_images}")
    print(f"   Items without images: {items_without_images}")
    print(f"   Success rate: {(items_with_images/len(menu_items)*100):.1f}%")
    
    # 3. Test URL generation
    print(f"\n3. URL Generation Test:")
    sample_item = menu_items.first()
    if sample_item:
        print(f"   Sample item: {sample_item.name}")
        print(f"   image_url property: {sample_item.image_url}")
        print(f"   get_image_url() method: {sample_item.get_image_url()}")
        print(f"   Category: {sample_item.get_dish_category()}")
        print(f"   Fallback URL: {sample_item.get_fallback_image_url()}")
    
    # 4. Test backend functionality
    print(f"\n4. Backend Functionality:")
    print(f"   Django DEBUG mode: {settings.DEBUG}")
    print(f"   Media serving configured: {'MEDIA_URL' in dir(settings)}")
    print(f"   Static files configured: {'STATIC_URL' in dir(settings)}")
    
    return items_with_images == len(menu_items)

def test_server_access():
    """Test if images are accessible via URLs"""
    print(f"\n=== SERVER ACCESS TEST ===")
    print("To test image serving, run these commands:")
    print("1. python manage.py runserver")
    print("2. Visit these URLs in browser:")
    
    menu_items = MenuItem.objects.all()[:3]  # Test first 3 items
    for item in menu_items:
        if item.has_image():
            print(f"   http://127.0.0.1:8000{item.image.url}")
    
    print("3. Visit the menu page:")
    print("   http://127.0.0.1:8000/menu/")

if __name__ == "__main__":
    success = test_imagefield_system()
    test_server_access()
    
    print(f"\n=== FINAL RESULT ===")
    if success:
        print("SUCCESS: All menu items have working ImageField images!")
        print("The backend is properly configured for ImageField handling.")
    else:
        print("WARNING: Some menu items are missing images.")
        print("Run 'python setup_menu_images.py' to fix missing images.")
    
    print(f"\nNext steps:")
    print("1. Start server: python manage.py runserver")
    print("2. Test menu page: http://127.0.0.1:8000/menu/")
    print("3. Verify images display correctly")
