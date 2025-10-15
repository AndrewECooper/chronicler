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

## Deployment

See the PRD.md for deployment instructions to Railway.app.

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
