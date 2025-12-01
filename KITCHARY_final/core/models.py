from django.db import models
from django.contrib.auth.models import User

# Menu items available for ordering
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)

    def __str__(self):
        return self.name
    
    @property
    def image_url(self):
        """Return the proper image URL using ImageField"""
        if self.image and hasattr(self.image, 'url'):
            return self.image.url
        else:
            # Fallback to static image
            return self.get_fallback_image_url()
    
    def get_image_url(self):
        """Get the image URL with fallback handling"""
        if self.image and hasattr(self.image, 'url'):
            try:
                # Check if image file exists
                import os
                from django.conf import settings
                image_path = os.path.join(settings.MEDIA_ROOT, str(self.image))
                if os.path.exists(image_path):
                    return self.image.url
            except:
                pass
        
        # Return fallback
        return self.get_fallback_image_url()
    
    def get_fallback_image_url(self):
        """Get a simple fallback image when no image is available"""
        return "data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMzAwIiBoZWlnaHQ9IjIwMCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cmVjdCB3aWR0aD0iMTAwJSIgaGVpZ2h0PSIxMDAlIiBmaWxsPSIjZjBmMGYwIi8+PHRleHQgeD0iMTUwIiB5PSIxMDAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNiIgZmlsbD0iIzY2NiI+SW5kaWFuIERpc2g8L3RleHQ+PC9zdmc+"
    
    def get_dish_category(self):
        """Determine the category of this dish"""
        name_lower = self.name.lower()
        
        if any(word in name_lower for word in ['pizza']):
            return 'pizza'
        elif any(word in name_lower for word in ['biryani', 'rice']):
            return 'biryani'
        elif any(word in name_lower for word in ['paneer', 'masala', 'curry', 'tikka']):
            return 'curry'
        elif any(word in name_lower for word in ['manchurian', 'chole', 'dosa', 'idli']):
            return 'snacks'
        elif any(word in name_lower for word in ['gulab', 'brownie', 'ice cream']):
            return 'dessert'
        elif any(word in name_lower for word in ['coffee', 'soda', 'drink']):
            return 'drinks'
        else:
            return 'snacks'
    
    def has_image(self):
        """Check if the menu item has a proper image"""
        return bool(self.image and hasattr(self.image, 'url'))
    
    def get_image_alt_text(self):
        """Get appropriate alt text for the image"""
        return f"Delicious {self.name} - {self.description[:50]}..." if self.description else f"Delicious {self.name}"

# Each order placed by a user
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(MenuItem, through='OrderItem')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    
    @property
    def total_price(self):
        return self.total_amount

# Intermediate table for item-quantity relationship in an order
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.menu_item.name}"


# Payment information associated with an order
class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')  # Add this if missing
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f'Payment {self.id} - {self.user.username}'

# User role (customer/staff/admin)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(
        max_length=20,
        choices=[
            ('admin', 'Admin'),
            ('customer', 'Customer'),
        ]
    )

    def __str__(self):
        return self.user.username
