from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import MenuItem

# --- Custom User Signup Form ---
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# --- Order Form with Quantity for each item ---
class OrderForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        menu_items = MenuItem.objects.all()
        self._menu_items = {}
        
        for item in menu_items:
            field_name = f'item_{item.id}'
            self._menu_items[field_name] = item
            self.fields[field_name] = forms.IntegerField(
                label=item.name,
                min_value=0,
                required=False,
                widget=forms.NumberInput(attrs={
                    'placeholder': 'Qty',
                    'style': 'width: 60px; padding: 5px; border: 1px solid #ddd; border-radius: 4px;'
                })
            )
    
    def get_menu_item_for_field(self, field):
        """Get the menu item associated with a form field"""
        return self._menu_items.get(field.name)

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username
