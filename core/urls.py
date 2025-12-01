from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu_view, name='menu'),

    # Auth
    path('signup/', views.signup_view, name='signup_view'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.custom_logout_view, name='logout'),

    # Dashboards
    path('', views.dashboard_redirect, name='dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/customer/', views.customer_dashboard, name='customer_dashboard'),

    # Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/place/', views.place_order, name='place_order'),
    path('orders/<int:order_id>/confirmation/', views.order_confirmation, name='order_confirmation'),

    # Payments
    path('payment/<int:order_id>/', views.make_payment, name='payment'),
    path('payment/success/<int:payment_id>/', views.payment_success, name='payment_success'),
    path('payments/', views.payment_list, name='payment_list'),
]
