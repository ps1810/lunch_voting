## 🥗 Lunch Voting App

A Django-based application for managing restaurant votes, with scheduled winner calculation using Celery and Redis. Built with clean architecture principles and Dockerized for easy deployment.

---

## 🚀 Features

- Add, update, delete restaurants
- Users vote on where to eat (weighted voting)
- Daily reset of votes
- Scheduled daily winner calculation
- Admin interface for managing data

---

## 🛠️ Getting Started

### 📦 Prerequisites

- Docker
- Docker Compose

---

### 🔧 Setup Instructions

1. **Clone the repo**

```bash
git clone https://github.com/ps1810/lunch-voting.git
cd lunch-voting
```

2. **Create a `.env` file**
```bash
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=*

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```
3. **Build and run the containers**

```bash
docker-compose up --build
```
4. **Run migrations & create superuser**

```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```
5. **Access the app**

```bash
Admin: http://localhost:8000/admin
```

## API Endpoints Summary

### Restaurants
- `GET /api/restaurants/` - List all restaurants
- `POST /api/restaurants/` - Create restaurant
- `GET /api/restaurants/{id}/` - Get restaurant details
- `PUT /api/restaurants/{id}/` - Update restaurant
- `DELETE /api/restaurants/{id}/` - Delete restaurant
- `GET /api/restaurants/search/?q=query` - Search restaurants
- `GET /api/restaurants/votable/` - Get restaurants user can vote for

### Voting
- `GET /api/votes/` - Get user's votes for today
- `POST /api/votes/` - Cast a vote

### Winners
- `GET /api/winners/?start_date=&end_date` - Get historical winners with optional date range
- `GET /api/winners/today/` - Get today's winner
- `POST /api/winners/calculate/?date=` - Force winner calculation

## API Authentication Guide

### Register a new user:
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser", 
    "password": "password123",
  }'
```

**Response:**
```json
{
  "token": "abc123def456...",
  "user_id": 1,
  "username": "testuser"
}
```

### Login existing user:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "password123"
  }'
```

### Use the token for authenticated requests:
```
# Save the token from login/register response
TOKEN="abc123def456..."
```

## Public Endpoints (No Authentication Required)

### Create a restaurant:
```bash
curl -X POST http://localhost:8000/api/restaurants/ \
  -H "Content-Type: application/json" \
  -d '{"name": "New Restaurant", "cuisine_type": "Italian", "phone": "01234...", "address":"Amsterdam"}'
```

### List all restaurants:
```bash
curl http://localhost:8000/api/restaurants/
```

### Get restaurant details:
```bash
curl http://localhost:8000/api/restaurants/1/
```

### Search restaurants:
```bash
curl http://localhost:8000/api/restaurants/search/?q=pizza
```

### Get restaurants you can vote for:
```bash
curl http://localhost:8000/api/restaurants/votable/
```

### Update a restaurant:
```bash
curl -X PUT http://localhost:8000/api/restaurants/1/ \
  -H "Content-Type: application/json" \
  -d '{"is_votable": false}'
```

### Delete a restaurant
```bash
curl -X DELETE http://localhost:8000/api/restaurants/1/
```

### Get today's winner:
```bash
curl http://localhost:8000/api/winners/today/
```

### Get historical winners:
```bash
curl http://localhost:8000/api/winners/?start_date=2023-01-01&end_date=2023-12-31
```

### Get all winners:
```bash
curl http://localhost:8000/api/winners/
```

### Force winner calculation:
```bash
curl -X POST http://localhost:8000/api/winners/calculate/?date=2025-01-01
```

## Protected Endpoints (Authentication Required)

### Vote for a restaurant
```bash
curl -X POST http://localhost:8000/api/votes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token $TOKEN" \
  -d '{"restaurant_id": 1}'
```

### Get votes for a user
```bash
curl -X GET http://localhost:8000/api/votes/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token $TOKEN"
```

### Logout (invalidates token):
```bash
curl -X POST \
  -H "Authorization: Token $TOKEN" \
  http://localhost:8000/api/auth/logout/
```