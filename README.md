# GymShop API

A complete Gym Shop backend built with Django and Django REST Framework.

## Features

- JWT Authentication
- Product Categories
- Brands
- Product Management
- Product Search
- Product Filtering
- Product Ordering
- Shopping Cart
- Order Management
- Product Reviews
- Admin Dashboard
- Swagger Documentation

---

## Tech Stack

- Python 3.13
- Django 6
- Django REST Framework
- Simple JWT
- SQLite
- drf-spectacular (Swagger)

---

## Installation

Clone project

```bash
git clone https://github.com/pouria-a2006/GymShop.git
```

Install packages

```bash
pip install -r requirements.txt
```

Apply migrations

```bash
python manage.py migrate
```

Run server

```bash
python manage.py runserver
```

---

## API Documentation

Swagger UI

```
http://127.0.0.1:8000/api/docs/
```

OpenAPI Schema

```
http://127.0.0.1:8000/api/schema/
```

---

## Main API Endpoints

### Authentication

```
POST /api/register/
POST /api/login/
POST /api/token/refresh/
POST /api/logout/
```

### Products

```
GET /api/products/
GET /api/products/{id}/
```

Supports

- Search
- Filtering
- Ordering
- Pagination

### Cart

```
GET /api/cart/
POST /api/cart/add/
PATCH /api/cart/item/{id}/
DELETE /api/cart/item/{id}/
```

### Orders

```
POST /api/orders/
GET /api/orders/
GET /api/orders/{id}/
```

### Reviews

```
GET /api/products/{id}/reviews/
POST /api/products/{id}/reviews/
```

---

## Authentication

This project uses JWT Authentication.

Example

```
Authorization: Bearer <access_token>
```

---

## Project Structure

```
shop/
    api/
    migrations/
    admin.py
    models.py
```

---

## Author

Pouria