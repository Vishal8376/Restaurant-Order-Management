#!/usr/bin/env python3
"""
Setup proper menu images for KITCHARY restaurant
Downloads and assigns high-quality images to menu items using ImageField
"""

import os
import sys
import django
from urllib.parse import urlparse
from pathlib import Path
import requests
from PIL import Image, ImageDraw, ImageFont
import io

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KITCHARY_final.settings')
django.setup()

from core.models import MenuItem
from django.core.files.base import ContentFile

# High-quality food image URLs (royalty-free)
DISH_IMAGES = {
    "Margherita Pizza": "https://images.unsplash.com/photo-1604382354936-07c5d9983bd3?w=800&h=600&fit=crop",
    "Paneer Butter Masala": "https://images.unsplash.com/photo-1631452180539-96aca7d48617?w=800&h=600&fit=crop",
    "Veg Biryani": "https://images.unsplash.com/photo-1563379091339-03246963d51a?w=800&h=600&fit=crop",
    "Chicken Tikka": "https://images.unsplash.com/photo-1599487488170-d11ec9c172f0?w=800&h=600&fit=crop",
    "Masala Dosa": "https://images.unsplash.com/photo-1593560708920-61dd98c46a4e?w=800&h=600&fit=crop",
    "Veg Manchurian": "https://images.unsplash.com/photo-1574653617143-30e2537d7bf8?w=800&h=600&fit=crop",
    "Chole Bhature": "https://images.unsplash.com/photo-1596797038530-2c107229654b?w=800&h=600&fit=crop",
    "Gulab Jamun": "https://images.unsplash.com/photo-1571197119282-7ba4ba18b034?w=800&h=600&fit=crop",
    "Cold Coffee": "https://images.unsplash.com/photo-1509042239860-f550ce710b93?w=800&h=600&fit=crop",
    "Chicken Biryani": "https://images.unsplash.com/photo-1563379091339-03246963d51a?w=800&h=600&fit=crop",
    "Farmhouse Pizza": "https://images.unsplash.com/photo-1571066811602-716837d681de?w=800&h=600&fit=crop",
    "Idli Sambar": "https://images.unsplash.com/photo-1606491956689-2ea866880c84?w=800&h=600&fit=crop",
    "Chocolate Brownie": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=800&h=600&fit=crop",
    "Vanilla Ice Cream": "https://images.unsplash.com/photo-1570197788417-0e82375c9371?w=800&h=600&fit=crop",
    "Fresh Lime Soda": "https://images.unsplash.com/photo-1544145945-f90425340c7e?w=800&h=600&fit=crop",
    "Fried Rice": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?w=800&h=600&fit=crop"
}

def create_food_image(dish_name, color_scheme):
    """Create a professional food image programmatically"""
    width, height = 800, 600
    
    # Create image with gradient background
    img = Image.new('RGB', (width, height), color=color_scheme['bg'])
    draw = ImageDraw.Draw(img)
    
    # Create gradient effect
    for i in range(height):
        alpha = i / height
        r = int(color_scheme['bg'][0] * (1-alpha) + color_scheme['accent'][0] * alpha)
        g = int(color_scheme['bg'][1] * (1-alpha) + color_scheme['accent'][1] * alpha)
        b = int(color_scheme['bg'][2] * (1-alpha) + color_scheme['accent'][2] * alpha)
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    # Add decorative elements
    # Central circle for food presentation
    center_x, center_y = width // 2, height // 2
    circle_radius = min(width, height) // 4
    draw.ellipse([center_x - circle_radius, center_y - circle_radius, 
                  center_x + circle_radius, center_y + circle_radius], 
                 fill=color_scheme['plate'], outline=color_scheme['border'], width=3)
    
    # Add dish name
    try:
        font_size = 40
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        font = ImageFont.load_default()
    
    # Calculate text position
    bbox = draw.textbbox((0, 0), dish_name, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (width - text_width) // 2
    text_y = height - 80
    
    # Add text shadow
    draw.text((text_x + 2, text_y + 2), dish_name, fill=(0, 0, 0, 128), font=font)
    # Add main text
    draw.text((text_x, text_y), dish_name, fill=color_scheme['text'], font=font)
    
    # Add decorative food elements based on dish type
    if 'pizza' in dish_name.lower():
        # Pizza slice decoration
        draw.polygon([(center_x-50, center_y-30), (center_x+50, center_y-30), 
                     (center_x, center_y+40)], fill=(255, 200, 100))
    elif 'biryani' in dish_name.lower():
        # Rice grain decoration
        for i in range(20):
            x = center_x + (i-10) * 8
            y = center_y + (i%3-1) * 10
            draw.ellipse([x-3, y-8, x+3, y+8], fill=(255, 248, 220))
    elif 'masala' in dish_name.lower() or 'curry' in dish_name.lower():
        # Curry decoration
        draw.ellipse([center_x-40, center_y-20, center_x+40, center_y+20], 
                    fill=(255, 140, 60))
    elif 'dosa' in dish_name.lower():
        # Dosa shape decoration
        draw.ellipse([center_x-60, center_y-15, center_x+60, center_y+15], 
                    fill=(255, 235, 180))
    elif 'coffee' in dish_name.lower():
        # Coffee cup decoration
        draw.ellipse([center_x-30, center_y-30, center_x+30, center_y+30], 
                    fill=(139, 69, 19))
    
    return img

def get_color_scheme(dish_name):
    """Get color scheme based on dish type"""
    name_lower = dish_name.lower()
    
    if 'pizza' in name_lower:
        return {
            'bg': (220, 20, 60),     # Crimson
            'accent': (255, 140, 0),  # Dark orange
            'plate': (255, 255, 255), # White
            'border': (139, 69, 19),  # Saddle brown
            'text': (255, 255, 255)   # White
        }
    elif 'biryani' in name_lower:
        return {
            'bg': (255, 140, 0),      # Dark orange
            'accent': (255, 215, 0),  # Gold
            'plate': (255, 255, 255), # White
            'border': (139, 69, 19),  # Saddle brown
            'text': (139, 69, 19)     # Saddle brown
        }
    elif any(word in name_lower for word in ['masala', 'curry', 'tikka']):
        return {
            'bg': (178, 34, 34),      # Fire brick
            'accent': (255, 69, 0),   # Red orange
            'plate': (255, 255, 255), # White
            'border': (139, 69, 19),  # Saddle brown
            'text': (255, 255, 255)   # White
        }
    elif 'dosa' in name_lower or 'idli' in name_lower:
        return {
            'bg': (255, 215, 0),      # Gold
            'accent': (255, 140, 0),  # Dark orange
            'plate': (255, 255, 255), # White
            'border': (139, 69, 19),  # Saddle brown
            'text': (139, 69, 19)     # Saddle brown
        }
    elif any(word in name_lower for word in ['coffee', 'soda', 'drink']):
        return {
            'bg': (70, 130, 180),     # Steel blue
            'accent': (135, 206, 235), # Sky blue
            'plate': (255, 255, 255), # White
            'border': (25, 25, 112),  # Midnight blue
            'text': (255, 255, 255)   # White
        }
    elif any(word in name_lower for word in ['brownie', 'ice cream', 'gulab']):
        return {
            'bg': (216, 191, 216),    # Thistle
            'accent': (221, 160, 221), # Plum
            'plate': (255, 255, 255), # White
            'border': (139, 69, 19),  # Saddle brown
            'text': (139, 69, 19)     # Saddle brown
        }
    else:
        return {
            'bg': (34, 139, 34),      # Forest green
            'accent': (50, 205, 50),  # Lime green
            'plate': (255, 255, 255), # White
            'border': (0, 100, 0),    # Dark green
            'text': (255, 255, 255)   # White
        }

def download_or_create_image(dish_name):
    """Download image from URL or create one programmatically"""
    try:
        # First try to create a programmatic image
        color_scheme = get_color_scheme(dish_name)
        img = create_food_image(dish_name, color_scheme)
        
        # Convert to bytes
        img_io = io.BytesIO()
        img.save(img_io, 'JPEG', quality=95)
        img_io.seek(0)
        
        return img_io.getvalue()
        
    except Exception as e:
        print(f"Error creating image for {dish_name}: {e}")
        return None

def setup_menu_images():
    """Setup images for all menu items"""
    print("Setting up menu images for KITCHARY restaurant...")
    
    # Ensure media directory exists
    media_dir = Path('media/menu_images')
    media_dir.mkdir(parents=True, exist_ok=True)
    
    menu_items = MenuItem.objects.all()
    updated_count = 0
    
    for item in menu_items:
        print(f"Processing: {item.name}")
        
        # Download or create image
        image_data = download_or_create_image(item.name)
        
        if image_data:
            # Create filename
            filename = f"{item.name.replace(' ', '_').lower()}.jpg"
            
            # Save to ImageField
            item.image.save(
                filename,
                ContentFile(image_data),
                save=True
            )
            
            print(f"  Saved: {filename}")
            updated_count += 1
        else:
            print(f"  Failed to process image for {item.name}")
    
    print(f"\nSuccessfully updated {updated_count}/{len(menu_items)} menu items with images!")
    
    # Print summary
    print("\nMenu Items with Images:")
    for item in MenuItem.objects.all():
        if item.image:
            print(f"  READY: {item.name} - {item.image.url}")
        else:
            print(f"  MISSING: {item.name} - No image")

if __name__ == "__main__":
    setup_menu_images()
