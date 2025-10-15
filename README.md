# The Chronicler

An advanced web-based AI-powered RPG gamemaster experience.

## Project Structure

```
Chronicler/
├── backend/           # FastAPI Python backend
│   ├── app/
│   │   └── main.py   # Main FastAPI application
│   └── requirements.txt
├── frontend/          # Vue 3 + Vite frontend
│   ├── src/
│   └── package.json
└── PRD.md            # Product Requirements Document
```

## Tech Stack

### Backend
- Python 3.11+
- FastAPI (async web framework)
- PostgreSQL (future)
- SQLAlchemy (future)

### Frontend
- Vue 3 (Composition API)
- Vite (build tool)
- Pinia (state management, future)
- Vue Router (future)

## Development Setup

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- npm or yarn

### Backend Setup

1. Create a virtual environment:
```bash
cd backend
python -m venv venv
```

2. Activate the virtual environment:
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the development server:
```bash
uvicorn app.main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`
- API documentation: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Running Both (Development)

You'll need two terminal windows:

**Terminal 1 (Backend):**
```bash
cd backend
venv\Scripts\activate  # or source venv/bin/activate on macOS/Linux
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

## Production Build

### Frontend
```bash
cd frontend
npm run build
```

This creates a `dist` folder with the production build.

### Backend
The FastAPI backend will automatically serve the frontend production build from the `dist` folder when it exists.

## Deployment to Railway

This project is configured for deployment to Railway.app with the following files:
- `railway.toml` - Railway build and deploy configuration
- `nixpacks.toml` - Nixpacks configuration for Python + Node.js
- `Procfile` - Alternative process configuration

### Deploy Steps

1. **Connect GitHub Repository**
   - Go to [Railway.app](https://railway.app)
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your Chronicler repository

2. **Configure Environment Variables** (optional for now)
   - No environment variables are required for the minimal setup
   - You'll need to add `DATABASE_URL`, `SECRET_KEY`, etc. later

3. **Deploy**
   - Railway will automatically detect the configuration files
   - The build process will:
     - Install Python dependencies from `backend/requirements.txt`
     - Install Node.js dependencies and build the frontend
     - Start the FastAPI server which serves both API and frontend

4. **Access Your App**
   - Railway will provide a URL like `https://chronicler-production.up.railway.app`
   - The health check endpoint: `https://your-app.railway.app/health`

### Railway Configuration Files

- **railway.toml**: Main Railway configuration
- **nixpacks.toml**: Tells Railway to use both Python 3.11 and Node.js 20
- **Procfile**: Specifies the start command for the web service

The deployment builds the frontend and serves it through the FastAPI backend, creating a single unified service.

## Current Status

This is the minimal starting point. The application currently displays a "Coming Soon" landing page.

Next steps:
- Set up PostgreSQL database
- Implement authentication system
- Create campaign management
- Build chat interface
- Develop agent system

## License

All rights reserved.
