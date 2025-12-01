#!/usr/bin/env python3
"""
Create realistic dish-specific images for KITCHARY restaurant menu
Generates authentic-looking images for each Indian dish
"""

import os
import sys
import django
from urllib.parse import urlparse
from pathlib import Path
import requests
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import math
import random

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'KITCHARY_final.settings')
django.setup()

from core.models import MenuItem
from django.core.files.base import ContentFile

def create_biryani_image(dish_name):
    """Create a realistic biryani image"""
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color=(139, 69, 19))  # Brown background
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for i in range(height):
        alpha = i / height
        r = int(139 * (1-alpha) + 255 * alpha * 0.8)
        g = int(69 * (1-alpha) + 215 * alpha * 0.8)
        b = int(19 * (1-alpha) + 0 * alpha * 0.8)
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    # Draw plate
    plate_center = (width//2, height//2 + 50)
    plate_radius = 180
    draw.ellipse([plate_center[0]-plate_radius, plate_center[1]-plate_radius,
                  plate_center[0]+plate_radius, plate_center[1]+plate_radius],
                 fill=(240, 240, 240), outline=(200, 200, 200), width=3)
    
    # Draw rice grains
    for i in range(150):
        x = plate_center[0] + random.randint(-150, 150)
        y = plate_center[1] + random.randint(-150, 150)
        if (x - plate_center[0])**2 + (y - plate_center[1])**2 <= 150**2:
            # Rice grain
            grain_length = random.randint(8, 12)
            grain_width = 3
            color = random.choice([(255, 248, 220), (255, 235, 180), (255, 215, 0)])
            draw.ellipse([x-grain_width, y-grain_length//2, x+grain_width, y+grain_length//2], fill=color)
    
    # Add some chicken pieces or vegetables
    for i in range(8):
        x = plate_center[0] + random.randint(-120, 120)
        y = plate_center[1] + random.randint(-120, 120)
        if (x - plate_center[0])**2 + (y - plate_center[1])**2 <= 120**2:
            if 'chicken' in dish_name.lower():
                # Chicken piece
                draw.ellipse([x-15, y-10, x+15, y+10], fill=(139, 69, 19))
            else:
                # Vegetable piece
                draw.ellipse([x-8, y-8, x+8, y+8], fill=(34, 139, 34))
    
    # Add title
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), dish_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) // 2
    text_y = 50
    
    # Text shadow
    draw.text((text_x + 2, text_y + 2), dish_name, fill=(0, 0, 0, 128), font=font)
    draw.text((text_x, text_y), dish_name, fill=(255, 255, 255), font=font)
    
    return img

def create_pizza_image(dish_name):
    """Create a realistic pizza image"""
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color=(139, 69, 19))  # Brown background
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for i in range(height):
        alpha = i / height
        r = int(139 * (1-alpha) + 205 * alpha)
        g = int(69 * (1-alpha) + 133 * alpha)
        b = int(19 * (1-alpha) + 63 * alpha)
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    # Draw pizza base
    center = (width//2, height//2 + 30)
    pizza_radius = 160
    draw.ellipse([center[0]-pizza_radius, center[1]-pizza_radius,
                  center[0]+pizza_radius, center[1]+pizza_radius],
                 fill=(255, 218, 185), outline=(210, 180, 140), width=8)
    
    # Draw tomato sauce
    sauce_radius = pizza_radius - 15
    draw.ellipse([center[0]-sauce_radius, center[1]-sauce_radius,
                  center[0]+sauce_radius, center[1]+sauce_radius],
                 fill=(220, 20, 60))
    
    # Draw cheese
    cheese_radius = sauce_radius - 5
    draw.ellipse([center[0]-cheese_radius, center[1]-cheese_radius,
                  center[0]+cheese_radius, center[1]+cheese_radius],
                 fill=(255, 255, 224), outline=(255, 215, 0), width=2)
    
    # Add toppings
    if 'margherita' in dish_name.lower():
        # Basil leaves
        for i in range(8):
            x = center[0] + random.randint(-100, 100)
            y = center[1] + random.randint(-100, 100)
            if (x - center[0])**2 + (y - center[1])**2 <= 100**2:
                draw.ellipse([x-8, y-6, x+8, y+6], fill=(34, 139, 34))
    elif 'farmhouse' in dish_name.lower():
        # Mixed vegetables
        for i in range(12):
            x = center[0] + random.randint(-100, 100)
            y = center[1] + random.randint(-100, 100)
            if (x - center[0])**2 + (y - center[1])**2 <= 100**2:
                color = random.choice([(255, 0, 0), (34, 139, 34), (255, 255, 0), (128, 0, 128)])
                draw.ellipse([x-6, y-6, x+6, y+6], fill=color)
    
    # Add title
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), dish_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) // 2
    text_y = 50
    
    draw.text((text_x + 2, text_y + 2), dish_name, fill=(0, 0, 0, 128), font=font)
    draw.text((text_x, text_y), dish_name, fill=(255, 255, 255), font=font)
    
    return img

def create_curry_image(dish_name):
    """Create a realistic curry image"""
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color=(178, 34, 34))
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for i in range(height):
        alpha = i / height
        r = int(178 * (1-alpha) + 255 * alpha * 0.7)
        g = int(34 * (1-alpha) + 140 * alpha * 0.7)
        b = int(34 * (1-alpha) + 0 * alpha * 0.7)
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    # Draw bowl
    bowl_center = (width//2, height//2 + 50)
    bowl_radius = 170
    draw.ellipse([bowl_center[0]-bowl_radius, bowl_center[1]-bowl_radius,
                  bowl_center[0]+bowl_radius, bowl_center[1]+bowl_radius],
                 fill=(139, 69, 19), outline=(101, 67, 33), width=8)
    
    # Draw curry
    curry_radius = bowl_radius - 20
    draw.ellipse([bowl_center[0]-curry_radius, bowl_center[1]-curry_radius,
                  bowl_center[0]+curry_radius, bowl_center[1]+curry_radius],
                 fill=(255, 140, 60))
    
    # Add curry pieces
    if 'paneer' in dish_name.lower():
        # Paneer cubes
        for i in range(12):
            x = bowl_center[0] + random.randint(-100, 100)
            y = bowl_center[1] + random.randint(-100, 100)
            if (x - bowl_center[0])**2 + (y - bowl_center[1])**2 <= 100**2:
                draw.rectangle([x-12, y-12, x+12, y+12], fill=(255, 255, 240))
    elif 'chicken' in dish_name.lower():
        # Chicken pieces
        for i in range(10):
            x = bowl_center[0] + random.randint(-100, 100)
            y = bowl_center[1] + random.randint(-100, 100)
            if (x - bowl_center[0])**2 + (y - bowl_center[1])**2 <= 100**2:
                draw.ellipse([x-15, y-12, x+15, y+12], fill=(139, 69, 19))
    
    # Add garnish
    for i in range(6):
        x = bowl_center[0] + random.randint(-80, 80)
        y = bowl_center[1] + random.randint(-80, 80)
        if (x - bowl_center[0])**2 + (y - bowl_center[1])**2 <= 80**2:
            draw.ellipse([x-4, y-4, x+4, y+4], fill=(34, 139, 34))
    
    # Add title
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), dish_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) // 2
    text_y = 50
    
    draw.text((text_x + 2, text_y + 2), dish_name, fill=(0, 0, 0, 128), font=font)
    draw.text((text_x, text_y), dish_name, fill=(255, 255, 255), font=font)
    
    return img

def create_dosa_image(dish_name):
    """Create a realistic dosa image"""
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color=(255, 215, 0))
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for i in range(height):
        alpha = i / height
        r = int(255 * (1-alpha) + 255 * alpha * 0.9)
        g = int(215 * (1-alpha) + 140 * alpha)
        b = int(0 * (1-alpha) + 0 * alpha)
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    # Draw banana leaf (plate)
    leaf_center = (width//2, height//2 + 50)
    draw.ellipse([leaf_center[0]-200, leaf_center[1]-120,
                  leaf_center[0]+200, leaf_center[1]+120],
                 fill=(34, 139, 34), outline=(0, 100, 0), width=3)
    
    # Draw dosa (rolled crepe)
    dosa_width = 250
    dosa_height = 40
    dosa_x = leaf_center[0] - dosa_width//2
    dosa_y = leaf_center[1] - dosa_height//2
    
    # Dosa shape (elongated oval)
    draw.ellipse([dosa_x, dosa_y, dosa_x + dosa_width, dosa_y + dosa_height],
                 fill=(255, 235, 180), outline=(218, 165, 32), width=3)
    
    # Add texture lines
    for i in range(5):
        y_pos = dosa_y + 8 + i * 6
        draw.line([(dosa_x + 20, y_pos), (dosa_x + dosa_width - 20, y_pos)], 
                 fill=(210, 180, 140), width=2)
    
    # Add sambar bowl
    sambar_x = leaf_center[0] + 100
    sambar_y = leaf_center[1] - 80
    draw.ellipse([sambar_x-40, sambar_y-30, sambar_x+40, sambar_y+30],
                 fill=(139, 69, 19), outline=(101, 67, 33), width=2)
    draw.ellipse([sambar_x-35, sambar_y-25, sambar_x+35, sambar_y+25],
                 fill=(255, 140, 0))
    
    # Add chutney bowl
    chutney_x = leaf_center[0] - 100
    chutney_y = leaf_center[1] - 80
    draw.ellipse([chutney_x-30, chutney_y-25, chutney_x+30, chutney_y+25],
                 fill=(139, 69, 19), outline=(101, 67, 33), width=2)
    draw.ellipse([chutney_x-25, chutney_y-20, chutney_x+25, chutney_y+20],
                 fill=(255, 255, 255))
    
    # Add title
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), dish_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) // 2
    text_y = 50
    
    draw.text((text_x + 2, text_y + 2), dish_name, fill=(0, 0, 0, 128), font=font)
    draw.text((text_x, text_y), dish_name, fill=(139, 69, 19), font=font)
    
    return img

def create_dessert_image(dish_name):
    """Create a realistic dessert image"""
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color=(216, 191, 216))
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for i in range(height):
        alpha = i / height
        r = int(216 * (1-alpha) + 255 * alpha * 0.9)
        g = int(191 * (1-alpha) + 160 * alpha)
        b = int(216 * (1-alpha) + 221 * alpha)
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    center = (width//2, height//2 + 30)
    
    if 'gulab jamun' in dish_name.lower():
        # Draw plate
        draw.ellipse([center[0]-120, center[1]-80, center[0]+120, center[1]+80],
                     fill=(255, 255, 255), outline=(200, 200, 200), width=3)
        
        # Draw gulab jamuns
        for i in range(6):
            angle = i * 60 * math.pi / 180
            x = center[0] + 50 * math.cos(angle)
            y = center[1] + 30 * math.sin(angle)
            draw.ellipse([x-25, y-20, x+25, y+20], fill=(139, 69, 19))
            # Syrup shine
            draw.ellipse([x-15, y-15, x+15, y+15], fill=(160, 82, 45), outline=(210, 180, 140), width=2)
    
    elif 'brownie' in dish_name.lower():
        # Draw brownie square
        brownie_size = 120
        draw.rectangle([center[0]-brownie_size//2, center[1]-brownie_size//2,
                       center[0]+brownie_size//2, center[1]+brownie_size//2],
                      fill=(101, 67, 33), outline=(139, 69, 19), width=3)
        
        # Add chocolate chips
        for i in range(15):
            x = center[0] + random.randint(-50, 50)
            y = center[1] + random.randint(-50, 50)
            draw.ellipse([x-4, y-4, x+4, y+4], fill=(0, 0, 0))
    
    elif 'ice cream' in dish_name.lower():
        # Draw bowl
        draw.ellipse([center[0]-80, center[1]-60, center[0]+80, center[1]+60],
                     fill=(255, 255, 255), outline=(200, 200, 200), width=3)
        
        # Draw ice cream scoops
        scoop_colors = [(255, 255, 224), (255, 182, 193), (173, 216, 230)]
        for i, color in enumerate(scoop_colors):
            y_offset = -40 + i * 25
            draw.ellipse([center[0]-40, center[1]+y_offset-30, center[0]+40, center[1]+y_offset+30],
                         fill=color, outline=(220, 220, 220), width=2)
    
    # Add title
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), dish_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) // 2
    text_y = 50
    
    draw.text((text_x + 2, text_y + 2), dish_name, fill=(0, 0, 0, 128), font=font)
    draw.text((text_x, text_y), dish_name, fill=(139, 69, 19), font=font)
    
    return img

def create_drink_image(dish_name):
    """Create a realistic drink image"""
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color=(70, 130, 180))
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for i in range(height):
        alpha = i / height
        r = int(70 * (1-alpha) + 135 * alpha)
        g = int(130 * (1-alpha) + 206 * alpha)
        b = int(180 * (1-alpha) + 235 * alpha)
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    center = (width//2, height//2 + 50)
    
    if 'coffee' in dish_name.lower():
        # Draw glass
        glass_width = 80
        glass_height = 150
        draw.rectangle([center[0]-glass_width//2, center[1]-glass_height//2,
                       center[0]+glass_width//2, center[1]+glass_height//2],
                      fill=(255, 255, 255, 150), outline=(200, 200, 200), width=3)
        
        # Draw coffee
        coffee_height = glass_height - 20
        draw.rectangle([center[0]-glass_width//2+5, center[1]+glass_height//2-coffee_height,
                       center[0]+glass_width//2-5, center[1]+glass_height//2-5],
                      fill=(139, 69, 19))
        
        # Whipped cream on top
        draw.ellipse([center[0]-30, center[1]-glass_height//2-10,
                     center[0]+30, center[1]-glass_height//2+20],
                    fill=(255, 255, 255))
        
        # Straw
        draw.rectangle([center[0]+20, center[1]-glass_height//2-30,
                       center[0]+25, center[1]-glass_height//2+100],
                      fill=(255, 0, 0))
    
    else:  # Soda
        # Draw glass
        glass_width = 70
        glass_height = 140
        draw.rectangle([center[0]-glass_width//2, center[1]-glass_height//2,
                       center[0]+glass_width//2, center[1]+glass_height//2],
                      fill=(255, 255, 255, 150), outline=(200, 200, 200), width=3)
        
        # Draw soda
        soda_height = glass_height - 20
        draw.rectangle([center[0]-glass_width//2+5, center[1]+glass_height//2-soda_height,
                       center[0]+glass_width//2-5, center[1]+glass_height//2-5],
                      fill=(50, 205, 50))
        
        # Bubbles
        for i in range(20):
            x = center[0] + random.randint(-25, 25)
            y = center[1] + random.randint(-60, 60)
            size = random.randint(2, 6)
            draw.ellipse([x-size//2, y-size//2, x+size//2, y+size//2],
                        fill=(255, 255, 255, 180))
        
        # Lime slice
        draw.ellipse([center[0]-15, center[1]-glass_height//2+10,
                     center[0]+15, center[1]-glass_height//2+40],
                    fill=(50, 205, 50), outline=(34, 139, 34), width=2)
    
    # Add title
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), dish_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) // 2
    text_y = 50
    
    draw.text((text_x + 2, text_y + 2), dish_name, fill=(0, 0, 0, 128), font=font)
    draw.text((text_x, text_y), dish_name, fill=(255, 255, 255), font=font)
    
    return img

def create_snacks_image(dish_name):
    """Create realistic snacks image"""
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color=(34, 139, 34))
    draw = ImageDraw.Draw(img)
    
    # Create gradient background
    for i in range(height):
        alpha = i / height
        r = int(34 * (1-alpha) + 50 * alpha)
        g = int(139 * (1-alpha) + 205 * alpha)
        b = int(34 * (1-alpha) + 50 * alpha)
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    center = (width//2, height//2 + 50)
    
    if 'chole bhature' in dish_name.lower():
        # Draw plate
        draw.ellipse([center[0]-150, center[1]-100, center[0]+150, center[1]+100],
                     fill=(255, 255, 255), outline=(200, 200, 200), width=3)
        
        # Draw bhature (puffed bread)
        draw.ellipse([center[0]-60, center[1]-40, center[0]+60, center[1]+40],
                     fill=(255, 235, 180), outline=(218, 165, 32), width=3)
        
        # Draw chole (chickpeas curry)
        draw.ellipse([center[0]+40, center[1]-30, center[0]+120, center[1]+50],
                     fill=(139, 69, 19))
        draw.ellipse([center[0]+45, center[1]-25, center[0]+115, center[1]+45],
                     fill=(255, 140, 0))
        
        # Add chickpeas
        for i in range(8):
            x = center[0] + 80 + random.randint(-25, 25)
            y = center[1] + 10 + random.randint(-25, 25)
            draw.ellipse([x-6, y-6, x+6, y+6], fill=(218, 165, 32))
    
    elif 'manchurian' in dish_name.lower():
        # Draw plate
        draw.ellipse([center[0]-120, center[1]-80, center[0]+120, center[1]+80],
                     fill=(255, 255, 255), outline=(200, 200, 200), width=3)
        
        # Draw manchurian balls
        for i in range(8):
            angle = i * 45 * math.pi / 180
            x = center[0] + 40 * math.cos(angle)
            y = center[1] + 25 * math.sin(angle)
            draw.ellipse([x-15, y-15, x+15, y+15], fill=(139, 69, 19))
            # Sauce glaze
            draw.ellipse([x-12, y-12, x+12, y+12], fill=(220, 20, 60), outline=(178, 34, 34), width=1)
    
    elif 'idli' in dish_name.lower():
        # Draw banana leaf
        draw.ellipse([center[0]-150, center[1]-100, center[0]+150, center[1]+100],
                     fill=(34, 139, 34), outline=(0, 100, 0), width=3)
        
        # Draw idlis (steamed cakes)
        idli_positions = [(center[0]-50, center[1]-30), (center[0]+50, center[1]-30), 
                         (center[0], center[1]+30)]
        for pos in idli_positions:
            draw.ellipse([pos[0]-25, pos[1]-15, pos[0]+25, pos[1]+15],
                         fill=(255, 255, 255), outline=(240, 240, 240), width=2)
        
        # Draw sambar bowl
        draw.ellipse([center[0]-80, center[1]+60, center[0]-20, center[1]+120],
                     fill=(139, 69, 19), outline=(101, 67, 33), width=2)
        draw.ellipse([center[0]-75, center[1]+65, center[0]-25, center[1]+115],
                     fill=(255, 140, 0))
    
    # Add title
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except:
        font = ImageFont.load_default()
    
    text_bbox = draw.textbbox((0, 0), dish_name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_x = (width - text_width) // 2
    text_y = 50
    
    draw.text((text_x + 2, text_y + 2), dish_name, fill=(0, 0, 0, 128), font=font)
    draw.text((text_x, text_y), dish_name, fill=(255, 255, 255), font=font)
    
    return img

def create_dish_specific_image(dish_name):
    """Create dish-specific realistic image"""
    name_lower = dish_name.lower()
    
    if any(word in name_lower for word in ['biryani', 'fried rice']):
        return create_biryani_image(dish_name)
    elif 'pizza' in name_lower:
        return create_pizza_image(dish_name)
    elif any(word in name_lower for word in ['paneer', 'masala', 'tikka']) and 'dosa' not in name_lower:
        return create_curry_image(dish_name)
    elif 'dosa' in name_lower:
        return create_dosa_image(dish_name)
    elif any(word in name_lower for word in ['gulab', 'brownie', 'ice cream']):
        return create_dessert_image(dish_name)
    elif any(word in name_lower for word in ['coffee', 'soda', 'drink']):
        return create_drink_image(dish_name)
    elif any(word in name_lower for word in ['chole', 'manchurian', 'idli']):
        return create_snacks_image(dish_name)
    else:
        return create_curry_image(dish_name)  # Default to curry style

def setup_realistic_dish_images():
    """Setup realistic dish-specific images"""
    print("Creating realistic dish-specific images for KITCHARY restaurant...")
    
    # Ensure media directory exists
    media_dir = Path('media/menu_images')
    media_dir.mkdir(parents=True, exist_ok=True)
    
    menu_items = MenuItem.objects.all()
    updated_count = 0
    
    for item in menu_items:
        print(f"Creating realistic image for: {item.name}")
        
        # Create dish-specific image
        img = create_dish_specific_image(item.name)
        
        # Convert to bytes
        img_io = io.BytesIO()
        img.save(img_io, 'JPEG', quality=95)
        img_io.seek(0)
        
        # Create filename
        filename = f"{item.name.replace(' ', '_').lower()}_realistic.jpg"
        
        # Save to ImageField
        item.image.save(
            filename,
            ContentFile(img_io.getvalue()),
            save=True
        )
        
        print(f"  Saved realistic image: {filename}")
        updated_count += 1
    
    print(f"\nSuccessfully created realistic images for {updated_count}/{len(menu_items)} dishes!")
    
    # Print summary
    print("\nRealistic Dish Images Created:")
    for item in MenuItem.objects.all():
        if item.image:
            print(f"  READY: {item.name} - {item.image.url}")
        else:
            print(f"  MISSING: {item.name} - No image")

if __name__ == "__main__":
    setup_realistic_dish_images()
