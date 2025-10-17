# 🚀 Smart Task Planner - Production Stack

> AI-powered project planning with Next.js, FastAPI, MongoDB, and AWS deployment ready

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Users / Browsers                          │
└───────────────┬─────────────────────────────────────────────┘
                │
        ┌───────▼────────┐
        │  CloudFront    │  (CDN - Optional)
        └───────┬────────┘
                │
    ┌───────────▼──────────────┐
    │   Application Load        │
    │   Balancer (ALB)          │
    └───────────┬──────────────┘
                │
        ┌───────▼────────┐
        │   ECS Fargate   │
        │   Containers    │
        └───────┬────────┘
                │
    ┌───────────▼──────────────────┐
    │  Next.js Frontend (Port 3000)│
    │  FastAPI Backend (Port 8000) │
    └───────────┬──────────────────┘
                │
        ┌───────▼────────┬──────────┐
        │                │          │
    ┌───▼───┐      ┌────▼────┐  ┌──▼──┐
    │MongoDB│      │ Gemini  │  │ S3  │
    │DocDB  │      │   API   │  │Bucket│
    └───────┘      └─────────┘  └─────┘
```

## 📦 Tech Stack

### Frontend
- **Next.js 14** - React framework with App Router
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **React Query** - Data fetching & caching
- **Axios** - HTTP client
- **Zod** - Schema validation

### Backend
- **FastAPI** - Modern Python API framework
- **MongoDB** (Motor + Beanie) - NoSQL database
- **Google Gemini AI** - Task generation
- **AWS S3** - File storage & exports
- **Pydantic** - Data validation

### Infrastructure
- **Docker** - Containerization
- **AWS ECS/Fargate** - Container orchestration
- **AWS DocumentDB** - MongoDB-compatible database
- **AWS S3** - Object storage
- **AWS CloudWatch** - Monitoring & logs

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+
- Python 3.13+
- MongoDB (local) or MongoDB Atlas
- Google Gemini API key

### 1. Clone Repository
```bash
git clone <repository-url>
cd smart_task_planner
```

### 2. Environment Setup

**Backend (.env)**
```bash
cd backend
cp .env.example .env
```

Edit `.env`:
```env
GEMINI_API_KEY=your-gemini-api-key
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=smart_task_planner
AWS_S3_BUCKET=your-bucket-name  # Optional
```

**Frontend (.env.local)**
```bash
cd frontend-next
cp .env.local.example .env.local
```

Edit `.env.local`:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_SECRET=generate-with-openssl-rand-base64-32
```

### 3. Run with Docker Compose

```bash
# From project root
docker-compose up --build
```

Services will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **MongoDB**: localhost:27017

### 4. Run Locally (Development)

**Terminal 1 - Backend**
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn backend.main:app --reload
```

**Terminal 2 - Frontend**
```bash
cd frontend-next
npm install
npm run dev
```

**Terminal 3 - MongoDB**
```bash
# Using Docker
docker run -d -p 27017:27017 --name mongodb mongo:7.0

# Or install MongoDB locally
```

## 📚 API Documentation

### Base URL
- Local: `http://localhost:8000`
- Production: `https://api.yourdomain.com`

### Key Endpoints

**Generate Plan**
```http
POST /api/plans/generate
Content-Type: application/json

{
  "goal_text": "Build a mobile app for habit tracking",
  "deadline": "2025-12-31",
  "max_hours_per_day": 6,
  "no_work_on_weekends": true,
  "plan_type": "moderate"
}
```

**Get Plan**
```http
GET /api/plans/{plan_id}
```

**Update Task**
```http
PUT /api/plans/{plan_id}/tasks/{task_id}
Content-Type: application/json

{
  "is_completed": true
}
```

**Export to S3**
```http
POST /api/plans/{plan_id}/export
```

See full API docs at: http://localhost:8000/docs

## 🐳 Docker Deployment

### Build Images
```bash
# Backend
docker build -t smart-planner-backend ./backend

# Frontend
docker build -t smart-planner-frontend ./frontend-next
```

### Push to Registry
```bash
# AWS ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker tag smart-planner-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/smart-planner-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/smart-planner-backend:latest

docker tag smart-planner-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/smart-planner-frontend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/smart-planner-frontend:latest
```

## ☁️ AWS Deployment

### 1. Setup MongoDB (DocumentDB)

```bash
# Create DocumentDB cluster
aws docdb create-db-cluster \
  --db-cluster-identifier smart-planner-cluster \
  --engine docdb \
  --master-username admin \
  --master-user-password YourSecurePassword123

# Create instance
aws docdb create-db-instance \
  --db-instance-identifier smart-planner-instance \
  --db-instance-class db.t3.medium \
  --engine docdb \
  --db-cluster-identifier smart-planner-cluster
```

Update `MONGODB_URL`:
```env
MONGODB_URL=mongodb://admin:password@smart-planner-cluster.cluster-xxx.us-east-1.docdb.amazonaws.com:27017/?tls=true&tlsCAFile=rds-combined-ca-bundle.pem&replicaSet=rs0
```

### 2. Setup S3 Bucket

```bash
# Create bucket
aws s3 mb s3://smart-planner-exports --region us-east-1

# Set CORS policy
aws s3api put-bucket-cors \
  --bucket smart-planner-exports \
  --cors-configuration file://s3-cors.json
```

### 3. Deploy to ECS/Fargate

```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name smart-planner-cluster

# Register task definitions
aws ecs register-task-definition --cli-input-json file://ecs-task-definition.json

# Create service
aws ecs create-service \
  --cluster smart-planner-cluster \
  --service-name smart-planner-service \
  --task-definition smart-planner:1 \
  --desired-count 2 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxx],securityGroups=[sg-xxx],assignPublicIp=ENABLED}"
```

### 4. Setup Load Balancer

```bash
# Create Application Load Balancer
aws elbv2 create-load-balancer \
  --name smart-planner-alb \
  --subnets subnet-xxx subnet-yyy \
  --security-groups sg-xxx

# Create target groups and listeners (see AWS docs)
```

## 📊 Monitoring & Logs

### CloudWatch Logs
```bash
# View logs
aws logs tail /ecs/smart-planner --follow
```

### Metrics
- CPU/Memory utilization
- Request count & latency
- Error rates
- Database connections

## 🔒 Security Checklist

- [ ] Environment variables in AWS Secrets Manager
- [ ] HTTPS only (SSL certificate via ACM)
- [ ] VPC with private subnets for database
- [ ] Security groups properly configured
- [ ] IAM roles with least privilege
- [ ] API rate limiting enabled
- [ ] CORS properly configured
- [ ] MongoDB authentication enabled
- [ ] S3 bucket policies restrictive

## 🧪 Testing

**Backend Tests**
```bash
cd backend
pytest
```

**Frontend Tests**
```bash
cd frontend-next
npm run test
```

## 📈 Scaling

### Horizontal Scaling
```bash
# Scale ECS service
aws ecs update-service \
  --cluster smart-planner-cluster \
  --service smart-planner-service \
  --desired-count 5
```

### Auto Scaling
```json
{
  "targetTrackingScalingPolicyConfiguration": {
    "targetValue": 75.0,
    "predefinedMetricSpecification": {
      "predefinedMetricType": "ECSServiceAverageCPUUtilization"
    }
  }
}
```

## 🐛 Troubleshooting

### MongoDB Connection Issues
```bash
# Test connection
mongosh "mongodb://localhost:27017/smart_task_planner"

# Check DocumentDB security group
# Ensure ECS tasks can reach DocumentDB on port 27017
```

### Gemini API Errors
```bash
# Verify API key
curl -H "Content-Type: application/json" \
  -d '{"contents":[{"parts":[{"text":"Hello"}]}]}' \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=YOUR_API_KEY"
```

### Container Issues
```bash
# View logs
docker logs smart-planner-backend

# Exec into container
docker exec -it smart-planner-backend /bin/sh
```

## 📝 License

MIT License - see LICENSE file

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📧 Support

- **Issues**: GitHub Issues
- **Email**: support@example.com
- **Docs**: https://docs.example.com

---

**Built with ❤️ using Next.js, FastAPI, MongoDB, and Google Gemini AI**
