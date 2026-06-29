# 🧱 LEGOShop — Django Pet Project

A full-featured online LEGO store built with Django. No payment processing — just a clean catalog, cart, auth system, and admin panel.

---

## Features

- **Catalog** — Products with categories, search, price filter
- **Cart** — Session-based cart (no login needed to browse)
- **Auth** — Register, login, logout, profile editor
- **Two Roles** — `client` and `admin`
- **Admin panel** (built-in, not Django admin):
  - Add / edit / delete products & categories
  - View and update all orders (status management)
  - Manage users (change role, deactivate, delete)
- **Orders** — Checkout, order history, order detail

---

## Quick Start

### 1. Clone / unzip the project

```bash
cd legoshop
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate        # Linux / Mac
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Seed demo data (optional but recommended)

```bash
python manage.py seed_data
```

This creates:
- 5 categories (City, Technic, Star Wars, Creator, Architecture)
- 16 demo LEGO products
- An admin account: **admin / admin123**

### 6. Start the server

```bash
python manage.py runserver
```

Visit **http://127.0.0.1:8000** 🎉

---

## Project Structure

```
legoshop/
├── manage.py
├── requirements.txt
└── legoshop/
    ├── settings.py
    ├── urls.py
    ├── accounts/       — Custom User model, auth views, user management
    ├── catalog/        — Products, categories, search
    ├── cart/           — Session-based cart
    ├── orders/         — Checkout, order history, admin order management
    ├── static/css/     — Custom CSS (no frameworks)
    └── templates/      — All HTML templates
```

---

## Roles

| Feature              | Client | Admin |
|----------------------|--------|-------|
| Browse catalog       | ✅     | ✅    |
| Add to cart          | ✅     | ✅    |
| Place orders         | ✅     | ✅    |
| View own orders      | ✅     | ✅    |
| View all orders      | ❌     | ✅    |
| Update order status  | ❌     | ✅    |
| Add/edit products    | ❌     | ✅    |
| Manage categories    | ❌     | ✅    |
| Manage users         | ❌     | ✅    |

---

## Creating an Admin User Manually

```bash
python manage.py createsuperuser
```

Then go to `/accounts/admin/users/` and change their role to `admin`.

Or use the Django admin at `/admin/` (superusers have full access).

---

## Adding Product Images

Upload images through the admin panel when creating/editing products. Images are stored in `media/products/`. If no image is provided, a 🧱 emoji placeholder is shown.

---

## Next Steps (ideas)

- Add product reviews / ratings
- Wishlist feature
- Stock management (decrement on order)
- Email confirmation on order
- Pagination for catalog
- REST API with DRF
