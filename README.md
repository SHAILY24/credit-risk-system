# Credit Risk System (CRS)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![React](https://img.shields.io/badge/react-18.2-blue.svg)
![Docker](https://img.shields.io/badge/docker-ready-green.svg)

## Overview

Credit Risk System (CRS) is an advanced, AI-powered credit risk assessment platform that leverages machine learning to provide accurate credit scoring and risk analysis. Built with modern technologies and best practices, it offers a comprehensive solution for financial institutions and lending platforms.

## Features

### Core Functionality
- **AI-Powered Risk Assessment**: Advanced machine learning models for accurate credit scoring
- **Real-time Predictions**: Instant credit risk evaluation with detailed insights
- **Historical Analysis**: Track and analyze prediction history and trends
- **API Key Management**: Secure API access with rate limiting and authentication
- **User Management**: Role-based access control with admin capabilities

### Technical Features
- **RESTful API**: Well-documented API endpoints for integration
- **Caching Layer**: Redis-powered caching for improved performance
- **Database Persistence**: PostgreSQL for reliable data storage
- **Containerized Deployment**: Docker-based architecture for easy deployment
- **SSL/TLS Support**: Built-in HTTPS configuration with Let's Encrypt
- **Monitoring Ready**: Prometheus and Grafana integration for system monitoring

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL 16
- **Cache**: Redis 7
- **ML Library**: Scikit-learn
- **Package Manager**: UV (Ultra-fast Python package manager)

### Frontend
- **Framework**: React 18 with TypeScript
- **UI Library**: Material-UI (MUI)
- **HTTP Client**: Axios
- **Build Tool**: Create React App

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Web Server**: Nginx
- **SSL**: Let's Encrypt with Certbot
- **Monitoring**: Prometheus & Grafana (optional)

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- Python 3.11+ (for local development)
- Node.js 20+ (for frontend development)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/SHAILY24/credit-risk-system.git
cd credit-risk-system
```

2. **Set up environment variables**
```bash
cp .env.production .env
# Edit .env with your configuration
```

3. **Start with Docker Compose**
```bash
docker compose up -d
```

4. **Access the application**
- Frontend: http://localhost:13960
- API Documentation: http://localhost:13960/api/docs
- Health Check: http://localhost:13960/health

## Live Demo

🌐 **Live Application**: https://crs.shaily.dev

### Demo Credentials
- **Username**: `admin`
- **Password**: `AdminCRS2024!@#`
- **Access**: Full admin privileges

Feel free to explore the application with these credentials. The demo resets periodically.

## Development Setup

### Backend Development
```bash
cd backend
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync
uvicorn app.main:app --reload --port 8000
```

### Frontend Development
```bash
cd frontend
yarn install
yarn start
```

### Database Setup
```bash
# Run migrations
docker compose exec backend python -m app.database

# Create admin user
docker compose exec backend python create_admin.py
```

## Production Deployment

### Using the Deployment Script
```bash
./deploy-production.sh
```

This script will:
- Check dependencies
- Generate secure secrets
- Obtain SSL certificates
- Build and deploy all services
- Set up automatic SSL renewal
- Create an admin user (optional)

### Manual Deployment

1. **Configure DNS**: Point your domain to your server
2. **Set environment variables**: Update `.env` with production values
3. **Run deployment**: `docker compose -f docker-compose.production.yml up -d`
4. **Set up SSL**: Run `./setup-host-nginx.sh` for nginx and SSL configuration

## API Documentation

### Authentication
The API uses JWT tokens for authentication. Obtain a token by logging in:

```bash
curl -X POST "https://crs.shaily.dev/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "your-username", "password": "your-password"}'
```

### Key Endpoints

- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user
- `POST /api/v1/predict` - Make credit risk prediction
- `GET /api/v1/predictions` - Get prediction history
- `GET /api/v1/api-keys` - Manage API keys

Full API documentation available at `/api/docs` when running the application.

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `REDIS_URL` | Redis connection string | Required |
| `SECRET_KEY` | JWT secret key | Auto-generated |
| `DEBUG` | Debug mode | false |
| `LOG_LEVEL` | Logging level | INFO |
| `CORS_ORIGINS` | Allowed CORS origins | http://localhost:3000 |

### Model Configuration

The credit risk model parameters are configured in `backend/model_info.json`:
- Feature definitions
- Risk thresholds
- Model metadata

## Monitoring

### Enable Monitoring Stack
```bash
docker compose --profile monitoring up -d
```

Access monitoring dashboards:
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3001 (admin/admin)

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
yarn test
```

### End-to-End Tests
```bash
# Test API endpoints
./test_backend.py

# Test model predictions
./test_features.py
```

## Security

- **Authentication**: JWT-based authentication with secure token handling
- **Rate Limiting**: API rate limiting to prevent abuse
- **Input Validation**: Comprehensive input validation and sanitization
- **HTTPS**: SSL/TLS encryption for all production traffic
- **CORS**: Configured CORS policies for API access
- **Secrets Management**: Environment-based secret configuration

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For issues, questions, or suggestions:
- Open an issue on [GitHub](https://github.com/SHAILY24/credit-risk-system/issues)
- Contact: admin@shaily.dev
- Documentation: [docs/](docs/)
- Live Demo: https://crs.shaily.dev

## Acknowledgments

- NJIT Data Mining Course for the foundational concepts
- FastAPI community for the excellent framework
- React community for the frontend tools
- All contributors and testers

---

**Built with ❤️ by [Shaily](https://github.com/SHAILY24)**

---

## Repository

- **GitHub**: https://github.com/SHAILY24/credit-risk-system
- **Live Demo**: https://crs.shaily.dev
- **License**: MIT