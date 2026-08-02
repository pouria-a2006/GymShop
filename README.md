## GymShop API

GymShop is a complete RESTful E-commerce Backend developed with **Django** and **Django REST Framework**.

The project follows an **API-first architecture**, making it suitable for web, mobile, or frontend frameworks such as React, Vue, Angular, Flutter, or any client capable of consuming REST APIs.

---

# Features

- JWT Authentication
- User Registration & Login
- Product Management
- Category Management
- Brand Management
- Product Search
- Product Filtering
- Product Ordering
- Pagination
- Shopping Cart
- Order Management
- Product Reviews
- Django Admin Panel
- Swagger API Documentation

---

# Technology Stack

- Python 3.13
- Django 6
- Django REST Framework
- SQLite
- Simple JWT
- django-filter
- drf-spectacular (Swagger/OpenAPI)

---

# Installation

Clone the repository

```bash
git clone https://github.com/pouria-a2006/GymShop.git
```

Go to project directory

```bash
cd GymShop
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Apply migrations

```bash
python manage.py migrate
```

Create superuser (optional)

```bash
python manage.py createsuperuser
```

Run server

```bash
python manage.py runserver
```

---

# API Documentation

Swagger UI

```
http://127.0.0.1:8000/api/docs/
```

OpenAPI Schema

```
http://127.0.0.1:8000/api/schema/
```

---

# Main API Endpoints

## Authentication

```
POST /api/register/
POST /api/login/
POST /api/token/refresh/
POST /api/logout/
```

---

## Products

```
GET /api/products/
GET /api/products/{id}/
```

Supports

- Search
- Filtering
- Ordering
- Pagination

---

## Shopping Cart

```
GET /api/cart/
POST /api/cart/add/
PATCH /api/cart/item/{id}/
DELETE /api/cart/item/{id}/
```

---

## Orders

```
POST /api/orders/
GET /api/orders/
GET /api/orders/{id}/
```

---

## Product Reviews

```
GET /api/products/{id}/reviews/
POST /api/products/{id}/reviews/
```

---

# Authentication

All protected endpoints require JWT Authentication.

Example

```
Authorization: Bearer <access_token>
```

---

# Project Structure

```
GymShop/
│
├── config/
├── shop/
│   ├── api/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
│
├── media/
├── manage.py
├── requirements.txt
└── README.md
```

---

# Testing

The project can be tested using:

- Swagger UI
- Postman
- Insomnia
- cURL

---

# License

This project is intended for educational and portfolio purposes.

---

# Author

**Pouria**

GitHub

https://github.com/pouria-a2006