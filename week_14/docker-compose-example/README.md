# Docker Compose Example: Express Backend + Next.js Frontend

This project demonstrates a microservices architecture with:
- **Backend**: Express.js API server running on port 5001
- **Frontend**: Next.js application running on port 3000

## Project Structure

```
docker-compose-example/
├── backend/
│   ├── app.js         # Express API server
│   ├── package.json   # Backend dependencies
│   └── Dockerfile     # Backend Docker configuration
├── frontend/
│   ├── app/
│   │   ├── page.js    # Main page component
│   │   └── layout.js  # Root layout
│   ├── package.json   # Frontend dependencies
│   ├── next.config.js # Next.js configuration
│   └── Dockerfile     # Frontend Docker configuration
└── docker-compose.yml # Docker Compose orchestration
```

## API Endpoints

Backend provides:
- `GET /api/message` - Returns a JSON message with timestamp
- `GET /health` - Health check endpoint

## Running with Docker Compose

### Build and start both services:

```bash
docker-compose up --build
```

### Run in detached mode (background):

```bash
docker-compose up -d --build
```

### Stop all services:

```bash
docker-compose down
```

### View logs:

```bash
docker-compose logs -f
```

## Access the Applications

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5001/api/message

## Development without Docker

### Backend:
```bash
cd backend
npm install
npm start
```

### Frontend:
```bash
cd frontend
npm install
npm run dev
```

Note: When running without Docker, update the API URL in the frontend to `http://localhost:5001`.