from django.contrib import admin
from .models import MenuItem, Order, Payment, OrderItem, UserProfile
from django.utils.html import format_html

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'image_preview', 'description_preview']
    list_filter = ['price']
    search_fields = ['name', 'description']
    fields = ['name', 'description', 'price', 'image', 'image_preview']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 60px; object-fit: cover; border-radius: 8px;" />',
                obj.image.url
            )
        return format_html(
            '<div style="width: 100px; height: 60px; background: #f0f0f0; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #666; font-size: 12px;">No Image</div>'
        )
    image_preview.short_description = 'Image Preview'
    
    def description_preview(self, obj):
        if obj.description:
            return obj.description[:50] + "..." if len(obj.description) > 50 else obj.description
        return "No description"
    description_preview.short_description = 'Description'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_amount', 'created_at', 'payment_status']
    list_filter = ['created_at']
    search_fields = ['user__username', 'id']
    readonly_fields = ['created_at']
    
    def payment_status(self, obj):
        payment = obj.payment_set.first()
        if payment:
            if payment.status == 'Completed':
                return format_html('<span style="color: green;">✅ Paid</span>')
            else:
                return format_html('<span style="color: orange;">⏳ Pending</span>')
        return format_html('<span style="color: red;">❌ No Payment</span>')
    payment_status.short_description = 'Payment Status'

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'order', 'amount', 'status', 'payment_date']
    list_filter = ['status', 'payment_date']
    search_fields = ['user__username', 'order__id']
    readonly_fields = ['payment_date']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'menu_item', 'quantity']
    list_filter = ['menu_item']
    search_fields = ['order__id', 'menu_item__name']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']
    list_filter = ['role']
    search_fields = ['user__username', 'user__email']