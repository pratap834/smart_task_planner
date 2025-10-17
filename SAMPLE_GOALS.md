# Sample Goals for Testing Smart Task Planner

## 1. Web Development Project
**Goal**: Build a full-stack e-commerce website with user authentication, product catalog, shopping cart, and payment integration

**Expected Tasks**:
- Project setup and architecture planning
- Database schema design
- Backend API development (authentication, products, cart, orders)
- Frontend UI development
- Payment gateway integration
- Testing and deployment

**Constraints**:
- Deadline: 30 days from now
- Max 8 hours per day
- No work on weekends

---

## 2. Learning Project
**Goal**: Learn Python and build a machine learning project to predict house prices

**Expected Tasks**:
- Learn Python basics
- Learn data analysis libraries (pandas, numpy)
- Learn machine learning concepts
- Data collection and preparation
- Model development and training
- Model evaluation and deployment

**Constraints**:
- Max 4 hours per day (learning mode)
- No work on weekends
- Conservative timeline

---

## 3. Content Creation
**Goal**: Write and publish a technical blog with 10 articles about software architecture

**Expected Tasks**:
- Blog platform setup
- Research topics and outline
- Write articles (10 articles)
- Edit and review
- Create diagrams and visuals
- Publish and promote

**Constraints**:
- Deadline: 20 days (aggressive)
- Max 6 hours per day
- Work on weekends allowed

---

## 4. Migration Project
**Goal**: Migrate legacy monolithic application to microservices architecture with Docker and Kubernetes

**Expected Tasks**:
- Analyze current architecture
- Design microservices architecture
- Set up infrastructure (Docker, K8s)
- Break down monolith into services
- Implement API gateway
- Database migration strategy
- Testing and gradual rollout
- Documentation

**Constraints**:
- Max 8 hours per day
- No work on weekends
- Moderate timeline

---

## 5. Mobile App Development
**Goal**: Create a React Native mobile app for habit tracking with local storage and notifications

**Expected Tasks**:
- Project setup and dependencies
- UI/UX design
- Implement habit management features
- Add notification system
- Implement local storage
- Testing on iOS and Android
- App store submission

---

## 6. DevOps Implementation
**Goal**: Set up complete CI/CD pipeline with automated testing, staging, and production deployment

**Expected Tasks**:
- Choose CI/CD platform
- Configure build pipeline
- Set up automated testing
- Configure staging environment
- Configure production deployment
- Add monitoring and alerts
- Documentation and training

---

## 7. Data Science Project
**Goal**: Build a recommendation system for a movie streaming platform using collaborative filtering

**Expected Tasks**:
- Data collection and exploration
- Data preprocessing and feature engineering
- Algorithm selection and implementation
- Model training and evaluation
- API development for recommendations
- Performance optimization
- Deployment

---

## 8. Business Process Automation
**Goal**: Automate invoice processing using Python, OCR, and database integration

**Expected Tasks**:
- Requirements gathering
- Set up OCR system
- Design database schema
- Implement invoice parsing logic
- Build validation system
- Create user interface
- Testing and refinement
- Deployment and training

---

## Usage Instructions

### Using the Web UI:
1. Open `frontend/index.html` in a browser
2. Paste any of the above goals into the text area
3. Set constraints as needed
4. Click "Generate Plan"

### Using the API Directly:
```bash
curl -X POST http://localhost:8000/api/plans \
  -H "Content-Type: application/json" \
  -d '{
    "goal_text": "Build a full-stack e-commerce website...",
    "plan_type": "moderate",
    "constraints": {
      "deadline": "2025-11-15",
      "max_hours_per_day": 8,
      "no_work_on_weekends": true
    }
  }'
```

### Using the Demo Script:
```bash
python demo_api.py
```

## Expected Output

Each plan will include:
- **Tasks**: 5-15 actionable tasks with IDs (T1, T2, etc.)
- **Dependencies**: Which tasks must be completed before others
- **Duration**: Estimated days for each task (1-3 days typical)
- **Dates**: Earliest start and latest finish dates
- **Priority**: High, Medium, or Low priority for each task
- **Confidence**: AI confidence score (0-1) for each estimate
- **Critical Path**: The sequence of tasks that determines minimum project duration
- **Plan Summary**: High-level overview and explanation

## Tips for Best Results

1. **Be Specific**: More detailed goals produce better task breakdowns
2. **Include Technologies**: Mention specific tools/frameworks you want to use
3. **Set Realistic Constraints**: Match constraints to your actual availability
4. **Review Dependencies**: Check that task dependencies make logical sense
5. **Adjust Timelines**: Use plan_type to control how aggressive the timeline is
