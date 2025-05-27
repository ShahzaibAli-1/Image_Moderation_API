# Image Moderation API

A FastAPI-based service for detecting and blocking harmful imagery using content moderation.

## Features

- Automatic detection of harmful content in images
- Bearer token authentication
- Admin-only endpoints for token management
- MongoDB integration for token and usage tracking
- Docker containerization
- Modern frontend UI for easy interaction

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── db/
│   │   └── services/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── .env.example
```

## Prerequisites

- Docker and Docker Compose
- Git
- MongoDB (if running locally)

## Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd image-moderation-api
```

2. Copy the example environment file and configure it:
```bash
cp .env.example .env
```

3. Build and run the containers:
```bash
docker-compose up --build
```

4. Access the services:
- Frontend: http://localhost:3000
- Backend API: http://localhost:7000
- API Documentation: http://localhost:7000/docs

## API Endpoints

### Authentication Endpoints (Admin-only)

- `POST /auth/tokens` - Generate new bearer token
- `GET /auth/tokens` - List all tokens
- `DELETE /auth/tokens/{token}` - Revoke specific token

### Moderation Endpoint

- `POST /moderate` - Submit image for content moderation

## Environment Variables

```env
# Backend
MONGODB_URI=mongodb://mongodb:27017
MONGODB_DB=image_moderation
JWT_SECRET=your-secret-key-here
ADMIN_TOKEN=admin-token-here

# Frontend
REACT_APP_API_URL=http://localhost:7000

# API Configuration
API_HOST=0.0.0.0
API_PORT=7000

# Frontend Configuration
FRONTEND_URL=http://localhost:3000
API_URL=http://localhost:7000
```

## Development

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 7000
```

### Frontend Development

```bash
cd frontend
npm install
npm start
```

## Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

## Docker Commands

- Build and start all services:
```bash
docker-compose up --build
```

- Stop all services:
```bash
docker-compose down
```

- View logs:
```bash
docker-compose logs -f
```

## Security Considerations

- All endpoints require valid bearer tokens
- Admin tokens are required for authentication endpoints
- Image content is analyzed for harmful content
- Usage tracking for all API calls

## Contributing

1. Create a feature branch (`git checkout -b feature/amazing-feature`)
2. Commit your changes (`git commit -m 'Add amazing feature'`)
3. Push to the branch (`git push origin feature/amazing-feature`)
4. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 