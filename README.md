# 🍽️ Restaurant Order Management System — Django

A complete web-based restaurant management platform built using **Django**.  
This system enables role-based access for **Manager, Customer, Chef, Waiter, and Supplier**, and provides features like menu browsing, order placement, inventory management, and payment tracking.

---

## 🚀 Features

### 🔐 Role-Based Authentication
- Separate dashboards for:
  - 👤 Customer — visually appealing UI to browse menu & place orders
  - 🛠️ Manager — professional interface to manage all restaurant operations
  - 👨‍🍳 Chef — view & update food preparation status
  - 🍽️ Waiter — manage table orders & delivery status
  - 🚚 Supplier — ingredient supply updates

### 🧾 Order Management
- Place food orders online
- Order history & status tracking
- View itemized order details

### 🍕 Menu Management
- Dynamic food menu display
- Add/Edit/Delete menu items (Manager access)

### 💳 Payment System
- Dummy payment gateway simulation
- Payment status linked to order

### 📦 Inventory & Kitchen Management
- Track ingredient availability
- Update stock based on orders
- Kitchen item requests

---

## 🏗️ Tech Stack

| Layer | Technology |
|------|------------|
| Backend | Django, Python |
| Frontend | HTML, CSS, JavaScript |
| Database | SQLite (default) — can be upgraded to PostgreSQL/MySQL |
| Authentication | Django Auth (Custom User Profiles) |

---

## 📂 Project Structure

