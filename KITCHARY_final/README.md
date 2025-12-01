# 🍽️ KITCHARY - Restaurant Food Ordering System

A full-stack Django web application for restaurant food ordering with user authentication, menu management, order processing, and payment handling.

## 🚀 Features

### 🔐 Authentication System
- **User Registration**: Custom signup with role selection (Customer/Admin)
- **User Login/Logout**: Secure authentication with Django's built-in system
- **Role-based Access**: Different dashboards for customers and admins

### 🍕 Menu Management
- **Visual Menu**: Display menu items with images, prices and descriptions
- **Image Support**: Upload and display dish images for better visual appeal
- **Order Placement**: Interactive form to select items and quantities with images
- **Real-time Calculations**: Automatic total calculation

### 📦 Order Management
- **Order Tracking**: Complete order history with status
- **Order Details**: View items, quantities, and total amounts
- **Order Confirmation**: Detailed confirmation page

### 💳 Payment System
- **Payment Processing**: Secure payment handling
- **Payment Status**: Track payment status (Pending/Completed)
- **Payment History**: Complete payment transaction history
- **Integration**: Seamless order-to-payment flow

### 👥 User Management
- **Customer Dashboard**: View orders, payments, and profile
- **Admin Dashboard**: System overview with analytics
- **User Profiles**: Automatic profile creation with role assignment

## 🛠️ Technology Stack

- **Backend**: Django 5.1.3
- **Database**: SQLite (production-ready, can be switched to PostgreSQL)
- **Frontend**: HTML5, CSS3, JavaScript (Bootstrap-style responsive design)
- **Authentication**: Django's built-in authentication system
- **Forms**: Django Forms with custom validation

## 📁 Project Structure

```
KITCHARY_final/
├── core/                          # Main application
│   ├── migrations/               # Database migrations
│   ├── templates/core/           # HTML templates
│   │   ├── base.html            # Base template
│   │   ├── login.html           # Login page
│   │   ├── signup.html          # Registration page
│   │   ├── menu.html            # Menu display
│   │   ├── place_order.html     # Order placement
│   │   ├── orders.html          # Order history
│   │   ├── make_payment.html    # Payment processing
│   │   ├── payments.html        # Payment history
│   │   ├── confirmation.html    # Order/Payment confirmation
│   │   ├── customer_dashboard.html
│   │   └── admin_dashboard.html
│   ├── models.py                # Database models
│   ├── views.py                 # View controllers
│   ├── forms.py                 # Form definitions
│   ├── urls.py                  # URL routing
│   └── admin.py                 # Admin interface
├── KITCHARY_final/              # Project settings
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Main URL configuration
│   └── wsgi.py                  # WSGI configuration
├── static/                      # Static files (CSS, JS, images)
├── db.sqlite3                   # Database file
├── manage.py                    # Django management script
├── setup_data.py               # Initial data setup
└── clean_data.py               # Database cleanup utility
```

## 🗄️ Database Models

### User Profile
- Extends Django's User model
- Role field (Customer/Admin)
- Automatic profile creation via signals

### Menu Item
- Name, description, price
- Image field for dish photos
- Used for order item selection

### Order
- User reference
- Total amount
- Created timestamp
- Many-to-many relationship with MenuItems

### Order Item
- Intermediate model for Order-MenuItem relationship
- Quantity field

### Payment
- User and Order references
- Amount and status
- Payment timestamp

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Step 1: Clone & Navigate
```bash
cd KITCHARY_final
```

### Step 2: Install Dependencies
```bash
pip install django
```

### Step 3: Database Setup
```bash
python manage.py migrate
```

### Step 4: Create Sample Data & Images
```bash
python clean_data.py
python add_sample_images.py
```

### Step 5: Run Development Server
```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000`

## 👤 Default Users

### Admin User
- **Username**: `admin`
- **Password**: `admin123`
- **Role**: Admin
- **Access**: Admin dashboard with system analytics

### Test Customers
Use the signup form to create customer accounts, or use existing ones:
- **Username**: `customer`
- **Password**: `customer123`

## 🧭 Application Flow

### Customer Journey
1. **Register/Login** → Choose Customer role
2. **Browse Menu** → View available food items
3. **Place Order** → Select items and quantities
4. **Make Payment** → Complete payment processing
5. **Order Confirmation** → Receive confirmation
6. **Track Orders** → View order and payment history

### Admin Journey
1. **Login** → Access admin dashboard
2. **View Analytics** → See total orders, revenue, etc.
3. **Manage System** → Access Django admin panel
4. **Monitor Payments** → Track payment status

## 🛡️ Security Features

- **CSRF Protection**: All forms protected against CSRF attacks
- **User Authentication**: Secure login/logout system
- **Role-based Access**: Different access levels for users
- **Data Validation**: Server-side form validation
- **Error Handling**: Graceful error handling and user feedback

## 🎨 UI/UX Features

- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern Interface**: Clean, professional design
- **User Feedback**: Success/error messages for all actions
- **Intuitive Navigation**: Easy-to-use navigation bar
- **Status Indicators**: Visual payment and order status

## 🔧 Customization

### Adding New Menu Items
1. Access Django admin panel: `/admin/`
2. Go to Menu Items section
3. Add new items with name, description, price, and upload images

### Modifying Styles
- Edit CSS in `core/templates/core/base.html`
- Add custom styles to individual templates

### Extending Functionality
- Add new models in `core/models.py`
- Create views in `core/views.py`
- Add URL patterns in `core/urls.py`

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
python manage.py runserver 8001
```

**Database Issues**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Missing Menu Items**
```bash
python clean_data.py
```

### Debug Mode
The application runs in DEBUG mode for development. For production:
1. Set `DEBUG = False` in `settings.py`
2. Configure `ALLOWED_HOSTS`
3. Use a production database (PostgreSQL)
4. Set up static file serving

## 📈 Future Enhancements

- **Real Payment Gateway**: Integrate Stripe/PayPal
- **Email Notifications**: Order confirmation emails
- **Order Status**: Real-time order tracking
- **Inventory Management**: Stock tracking
- **Delivery Integration**: GPS tracking
- **Reviews & Ratings**: Customer feedback system
- **Promotions**: Discount codes and offers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open-source and available under the MIT License.

## 📞 Support

For issues or questions:
- Check the troubleshooting section
- Review Django documentation
- Create an issue in the repository

---

Built with ❤️ using Django
