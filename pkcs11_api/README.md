# CloudHSM Management Dashboard Backend

FastAPI backend for CloudHSM operations using PyKCS11.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment:
```bash
cp .env.example .env
# Edit .env with your CloudHSM configuration
```

3. Run the application:
```bash
python main.py
```

## Testing the Login Endpoint

```bash
# Test login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "crypto-user", "password": "your-password"}' \
  -v

# Test logout
curl -X POST "http://localhost:8000/api/v1/auth/logout" \
  -H "Content-Type: application/json" \
  -v
```

## API Documentation

Once running, visit:
- API docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health