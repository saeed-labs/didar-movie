# 🎬 Didar Movie Backend

A RESTful backend for **Didar Movie**, a movie streaming and digital movie purchasing platform built with Django and Django REST Framework.

The project provides APIs for user authentication, movie catalog management, categories, shopping cart, movie ownership, payments, subscriptions, and protected API documentation.

The application is containerized with Docker Compose and uses PostgreSQL as its primary database, Gunicorn as the WSGI server, and Nginx as a reverse proxy.

---

## ✨ Features

- 🔐 Custom user model and authentication
- 🔑 JWT-based authentication with access and refresh tokens
- 📱 User registration and OTP verification
- 🎬 Movie catalog and movie details
- 🎭 Actors and directors
- 🏷️ Genres and movie categorization
- 🔎 Filtering movies by genre, actor, and director
- 🛒 Shopping cart
- 🎟️ Movie ownership after successful payment
- 💳 Payment processing with ZarinPal
- 💰 Subscription plans and subscription payments
- 📚 OpenAPI schema and Swagger UI
- 🛡️ Custom permissions for movie ownership
- 📦 PostgreSQL database
- 🐳 Dockerized development and deployment
- 🌐 Nginx reverse proxy
- 📁 Separate media and static file volumes
- 🚀 Gunicorn production server
- 🔒 HTTP Basic Authentication for Swagger and Django Admin

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.14 | Programming language |
| Django 6.1 | Web framework |
| Django REST Framework | REST API |
| Simple JWT | JWT authentication |
| PostgreSQL 18 | Database |
| Gunicorn | WSGI application server |
| Nginx | Reverse proxy & static/media serving |
| Docker | Containerization |
| drf-spectacular | OpenAPI / Swagger documentation |
| Pillow | Image processing |
| ZarinPal | Payment gateway |

The exact Python and package versions are pinned in `app/requirements.txt`.

---

## 🏗️ Architecture

The application uses a simple containerized architecture:

```text
                    ┌──────────────────┐
                    │      Client      │
                    │ Flutter / Web /  │
                    │     Mobile       │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │      Nginx       │
                    │   Reverse Proxy  │
                    └────────┬─────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │     Gunicorn     │
                    │      Django      │
                    │       API        │
                    └────────┬─────────┘
                             │
                 ┌───────────┴───────────┐
                 ▼                       ▼
        ┌─────────────────┐     ┌─────────────────┐
        │   PostgreSQL    │     │ Media / Static  │
        │     Database    │     │     Volumes     │
        └─────────────────┘     └─────────────────┘
```

Docker Compose defines three services:

- `app` → Django + Gunicorn
- `postgres` → PostgreSQL 18
- `nginx` → Reverse proxy and static/media server

The application container exposes port `8000` internally, while Nginx exposes port `80`. PostgreSQL is also mapped to port `5432`.

---

## 📁 Project Structure

```text
didar-movie-backend/
│
├── app/
│   ├── accounts/
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── manager.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── cart/
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── categories/
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── config/
│   │   ├── settings/
│   │   │   ├── conf/
│   │   │   │   ├── apps_conf.py
│   │   │   │   ├── db_conf.py
│   │   │   │   ├── devlopment.py
│   │   │   │   ├── meddleware_conf.py
│   │   │   │   ├── paths.py
│   │   │   │   └── production.py
│   │   │   ├── base.py
│   │   │   └── __init__.py
│   │   │
│   │   ├── urls/
│   │   │   ├── urls.py
│   │   │   └── v1.py
│   │   │
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   ├── home/
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── middleware/
│   │   └── erorr_status.py
│   │
│   ├── movies/
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── filters.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── payment/
│   │   ├── migrations/
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   └── views.py
│   │
│   ├── permissions/
│   │   └── movie_owner.py
│   │
│   ├── utils/
│   │   ├── gateways/
│   │   │   ├── services.py
│   │   │   └── zarinpal.py
│   │   ├── customPagination.py
│   │   └── send_email.py
│   │
│   ├── Dockerfile
│   ├── entrypoint.sh
│   ├── manage.py
│   └── requirements.txt
│
├── nginx/
│   ├── Dockerfile
│   ├── default.conf
│   ├── errors.inc
│   ├── locations.inc
│   └── upstream.inc
│
├── volumes/
│   ├── assets/
│   ├── dbdata/
│   └── media/
│
├── .gitignore
└── docker-compose.yaml
```

The structure above follows the current repository layout. The Django application is split into domain-oriented apps rather than putting the entire API into a single application.

---

## 📦 Django Applications

### `accounts`

Responsible for the custom user system and authentication flow.

Main responsibilities:

- Custom `User` model
- User manager
- Registration
- Login
- OTP verification
- User profile
- JWT authentication

Authentication endpoints include:

```text
/v1/user/
/v1/user/login/
/v1/user/login/verify-otp/
/v1/user/register/
/v1/user/register/verify/
```

The authentication routes are defined in `accounts/urls.py`.

---

### `movies`

The main movie catalog application.

Responsibilities include:

- Movie models
- Movie videos
- Genres
- Actors
- Directors
- Movie filtering
- Movie list and detail APIs
- Movie metadata
- Pagination

Main endpoints:

```text
/v1/movie/
/v1/movie/<id>/<slug>/
```

Movie filtering is implemented separately in `filters.py`.

---

### `categories`

Provides endpoints for retrieving movies through related categories.

Supported relationships:

```text
Genre → Movies
Actor → Movies
Director → Movies
```

Endpoints:

```text
/v1/categories/genres/<genre_id>/movies/
/v1/categories/actors/<actor_id>/movies/
/v1/categories/directors/<director_id>/movies/
```



---

### `cart`

Handles the user's shopping cart.

Features:

- View cart
- Add movie to cart
- Apply coupon

Endpoints:

```text
/v1/cart/
/v1/cart/add/<movie_id>/
/v1/cart/coupon/apply/
```



---

### `payment`

Handles the payment workflow.

Features:

- Movie purchase
- ZarinPal payment
- Payment callback
- Subscription plans
- Subscription payments
- Movie ownership after successful payment

Endpoints:

```text
/v1/payment/request/
/v1/payment/zarinpal/callback/
/v1/payment/subscription/plans/
/v1/payment/subscription/plans/<id>/
```



---

### `permissions`

Contains custom DRF permissions.

Currently, the project includes a movie ownership permission:

```text
permissions/movie_owner.py
```

This can be used to restrict access to movies that a user has purchased.



---

### `utils`

Contains reusable application utilities.

```text
utils/
├── gateways/
│   ├── services.py
│   └── zarinpal.py
├── customPagination.py
└── send_email.py
```

The `gateways` package separates payment gateway logic from the API views, while pagination and email functionality are kept as reusable utilities.

---

## 🔐 Authentication

The API uses **JWT authentication** through `djangorestframework-simplejwt`.

Configuration includes:

- Access token lifetime: 30 minutes
- Refresh token lifetime: 180 days
- Refresh token rotation
- Refresh token blacklisting
- `Bearer` authentication scheme

Example:

```http
Authorization: Bearer <access_token>
```



---

## 📚 API Documentation

The project uses `drf-spectacular` to generate an OpenAPI schema.

Swagger UI:

```text
http://localhost/v1/api/schema/swagger-ui/
```

OpenAPI schema:

```text
http://localhost/v1/api/schema/
```

Swagger is protected by HTTP Basic Authentication at the Nginx level.

The Django Admin is also protected by HTTP Basic Authentication through Nginx:

```text
http://localhost/v1/admin-panel/
```



---

# 🚀 Getting Started

## Requirements

The recommended way to run the project is using Docker.

Install:

- Docker
- Docker Compose

No local Python or PostgreSQL installation is required when using the Docker setup.

The backend image currently uses Python `3.14.6`.

---

## 1. Clone the repository

```bash
git clone https://github.com/saeed-labs/didar-movie-backend.git
cd didar-movie-backend
```

---

## 2. Create the environment file

Create a `.env` file in the project root:

```bash
touch .env
```

The project reads database configuration and other sensitive settings from environment variables.

A minimal configuration for local development can look like:

```env
# Django
DJANGO_SECRET_KEY=change-this-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1

# PostgreSQL
DB_NAME=saeed_db
DB_USER=saeed_user
DB_PASSWORD=change-this-password
DB_HOST=postgres

# Email
DJANGO_EMAIL_HOST=smtp.example.com
DJANGO_EMAIL_PORT=587
DJANGO_EMAIL_HOST_USER=your-email@example.com
DJANGO_EMAIL_HOST_PASSWORD=your-password
DJANGO_EMAIL_USE_TLS=True
DJANGO_DEFAULT_FROM_EMAIL=your-email@example.com

# ZarinPal
ZARINPAL_MERCHANT_ID=your-merchant-id
ZARINPAL_SANDBOX=True
```

The database configuration uses `DB_NAME`, `DB_USER`, `DB_PASSWORD`, and `DB_HOST`.

Production configuration also reads Django, email, and ZarinPal settings from environment variables.

> **Important:** Never commit your real `.env` file, passwords, API keys, email credentials, or payment gateway credentials to Git.

---

## 3. Configure Nginx credentials

The Nginx container expects:

```text
nginx/.htpasswd
```

This file is used to protect:

```text
/v1/api/schema/
/v1/admin-panel/
```

Create it with:

```bash
mkdir -p nginx

docker run --rm \
  httpd:2.4-alpine \
  htpasswd -nbB admin your-password > nginx/.htpasswd
```

Replace `admin` and `your-password` with your desired credentials.

---

## 4. Build and start the project

Run:

```bash
docker compose up --build
```

Or run it in detached mode:

```bash
docker compose up --build -d
```

Docker Compose starts:

```text
app
postgres
nginx
```

The PostgreSQL service has a health check, and the Django application waits for PostgreSQL to become healthy before starting.

---

## 5. Access the application

Once the containers are running:

### API

```text
http://localhost/v1/
```

### Swagger

```text
http://localhost/v1/api/schema/swagger-ui/
```

### Django Admin

```text
http://localhost/v1/admin-panel/
```

### Static files

```text
http://localhost/assets/
```

### Media files

```text
http://localhost/media/
```

Nginx serves `/assets/` and `/media/` directly from the mounted Docker volumes.

---

# 👤 Default Admin User

During container startup, `entrypoint.sh` checks whether any users exist.

If the database has no users, it automatically creates a superuser:

```text
Email:    admin@example.com
Username: admin
Phone:    09123456789
Password: admin
```

This behavior is implemented directly in the startup script.

### ⚠️ Security Warning

These credentials are suitable only for local development.

**Change or remove this automatic superuser creation before deploying the application to production.**

---

# 🗄️ Database & Persistence

PostgreSQL data is persisted through:

```text
volumes/dbdata/
```

Media files are stored in:

```text
volumes/media/
```

Static files are stored in:

```text
volumes/assets/
```

Docker Compose mounts these directories into the corresponding containers, allowing application data to survive container recreation.

---

# 🔄 Container Startup

The Django container runs `entrypoint.sh` before starting Gunicorn.

The startup sequence is:

```text
1. makemigrations
2. migrate
3. collectstatic
4. Create initial superuser if no users exist
5. Start Gunicorn
```

The final application process is:

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000
```



---

# 🌐 Nginx

Nginx acts as the reverse proxy in front of Django.

Traffic flow:

```text
Client
  │
  ▼
Nginx :80
  │
  ▼
Django / Gunicorn :8000
```

The upstream configuration points Nginx to:

```text
app:8000
```



Nginx also handles:

- Reverse proxying API requests
- Static files
- Media files
- Swagger authentication
- Admin authentication
- Request body size up to 100 MB



---

# 🔗 API Overview

All API endpoints are versioned under:

```text
/v1/
```

Current route groups:

| Prefix | Description |
|---|---|
| `/v1/home/` | Home-related APIs |
| `/v1/user/` | Authentication and users |
| `/v1/movie/` | Movies |
| `/v1/categories/` | Movie categories |
| `/v1/cart/` | Shopping cart |
| `/v1/payment/` | Payments and subscriptions |
| `/v1/api/schema/` | OpenAPI schema |
| `/v1/admin-panel/` | Django Admin |



---

# 🧪 Development

To access the Django container:

```bash
docker compose exec app sh
```

Run Django management commands:

```bash
docker compose exec app python manage.py shell
```

Create migrations manually if needed:

```bash
docker compose exec app python manage.py makemigrations
```

Apply migrations:

```bash
docker compose exec app python manage.py migrate
```

Collect static files:

```bash
docker compose exec app python manage.py collectstatic
```

Create a superuser manually:

```bash
docker compose exec app python manage.py createsuperuser
```

---

# 📋 Useful Docker Commands

### Start

```bash
docker compose up -d
```

### Stop

```bash
docker compose down
```

### Rebuild

```bash
docker compose up --build -d
```

### View logs

```bash
docker compose logs -f
```

### Django logs only

```bash
docker compose logs -f app
```

### Nginx logs

```bash
docker compose logs -f nginx
```

### PostgreSQL logs

```bash
docker compose logs -f postgres
```

### Check running containers

```bash
docker compose ps
```

---

# 🧹 Reset Development Environment

> ⚠️ This removes the PostgreSQL data stored in the local volume.

Stop the containers:

```bash
docker compose down
```

Remove the local database volume:

```bash
rm -rf volumes/dbdata
```

Start the project again:

```bash
docker compose up --build -d
```

---

# 🔒 Security Notes

Before deploying to production:

- Change the default superuser credentials.
- Use a strong `DJANGO_SECRET_KEY`.
- Set `DJANGO_DEBUG=False`.
- Configure `DJANGO_ALLOWED_HOSTS`.
- Use HTTPS.
- Replace development ZarinPal settings with production credentials.
- Keep `.env` outside version control.
- Use strong Nginx Basic Auth credentials.
- Review file upload limits.
- Configure secure proxy/SSL settings.
- Do not expose PostgreSQL publicly unless required.
- Rotate credentials if they have ever been committed to Git.

---

# 📌 Project Status

Didar Movie Backend is an ongoing project and is primarily intended as a practical backend project for a movie streaming and digital content platform.

The architecture is designed to provide a foundation for a future mobile or web frontend while keeping business domains separated into independent Django applications.

---

## 📄 License

No license has currently been specified for this repository.

If you intend to make the project open source, add an appropriate `LICENSE` file to the repository.

---

## 👨‍💻 Author

**Saeed**

GitHub:

https://github.com/saeed-labs

Repository:

https://github.com/saeed-labs/didar-movie-backend