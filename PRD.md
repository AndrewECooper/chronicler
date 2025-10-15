# The Chronicler - Product Requirements Document (Web Application)

## Overview
An advanced web-based AI-powered RPG gamemaster experience. This application addresses the core challenges of AI-driven tabletop gaming through specialized agent systems and intelligent game state management, now accessible from any device with a modern browser.

## Target Audience
- **Primary**: Experienced tabletop RPG players and gamemasters
- **Secondary**: Solo RPG enthusiasts
- **Tertiary**: RPG groups seeking AI assistance
- **Expanded**: Remote RPG groups, mobile users, casual players without installation barriers

## Core Problem Statement
Current AI systems struggle with three critical gamemaster functions:

1. **Excessive Agreeability**: AI tends to let players succeed too easily, reducing challenge and engagement
2. **Mechanical Awareness**: AI fails to recognize when narrative actions should trigger game mechanics (dice rolls, skill checks)
3. **Long-term Continuity**: AI cannot maintain consistent NPC motivations, goals, and story threads across sessions

## Core Objectives
1. Create an AI gamemaster that provides appropriate challenge and resistance
2. Seamlessly integrate narrative gameplay with mechanical systems
3. Maintain persistent, consistent world state and character continuity
4. Provide a superior RPG experience compared to standard AI chat interfaces
5. **NEW**: Enable multi-device access and cloud-based campaign persistence
6. **NEW**: Support multiple users with secure data isolation

## Technical Specifications

### Technology Stack

#### Backend
- **Language**: Python 3.11+
- **Web Framework**: FastAPI (async, high-performance)
- **Database**: PostgreSQL 15+ with JSONB support
- **ORM**: SQLAlchemy 2.0 with Alembic migrations
- **API Client**: Anthropic Python SDK
- **Authentication**: JWT tokens with bcrypt password hashing
- **API Documentation**: Auto-generated OpenAPI/Swagger via FastAPI

#### Frontend
- **Framework**: Vue 3 (Composition API)
- **Build Tool**: Vite
- **State Management**: Pinia (lightweight, Vue 3 native)
- **Routing**: Vue Router
- **HTTP Client**: Fetch API (native) with error handling wrapper
- **Styling**: CSS3 with scoped component styles
- **Real-time**: Server-Sent Events (SSE) for streaming AI responses

#### Infrastructure
- **Hosting**: Railway.app
- **Database**: Railway PostgreSQL instance
- **Deployment**: Git-based CI/CD (automatic on push to main)
- **Environment**: Development, Staging, Production environments
- **Monitoring**: Railway built-in metrics + logs

#### Development Tools
- **Backend**: uvicorn (ASGI server), pytest (testing), black (formatting)
- **Frontend**: ESLint (linting), Prettier (formatting), Vitest (testing)
- **API Testing**: FastAPI TestClient, Postman/Thunder Client

### Architecture Diagram
```
┌─────────────────────────────────────┐
│  Frontend (Vue 3 + Vite)            │
│  - Campaign Management UI           │
│  - Chat Interface                   │
│  - Real-time Streaming              │
└──────────────┬──────────────────────┘
               │ HTTPS/SSE
┌──────────────▼──────────────────────┐
│  Backend API (FastAPI)              │
│  - REST Endpoints                   │
│  - Authentication & Authorization   │
│  - Agent Pipeline Processing        │
│  - Streaming Response Handler       │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  Agent System (Python)              │
│  - Entity Agent (ported from JS)    │
│  - Mechanics Agent                  │
│  - Antagonist Agent                 │
│  - Continuity Agent                 │
└──────────────┬──────────────────────┘
               │
┌──────────────▼──────────────────────┐
│  PostgreSQL Database                │
│  - Users & Authentication           │
│  - Campaigns & Sessions             │
│  - Chats & Messages                 │
│  - NPCs & Entities (JSONB)          │
│  - Plot Threads & Game State        │
└─────────────────────────────────────┘
```

## Data Models

### Database Schema

#### Users
```python
class User(Base):
    id: UUID (primary key)
    email: str (unique, indexed)
    password_hash: str
    display_name: str
    api_key_encrypted: str (user's Claude API key)
    created_at: datetime
    last_login: datetime
    preferences: JSONB (theme, model, etc.)
```

#### Campaigns
```python
class Campaign(Base):
    id: UUID (primary key)
    user_id: UUID (foreign key → Users)
    title: str
    system: str (e.g., "D&D 5e", "Generic", "Pathfinder")
    description: str
    game_state: JSONB (flexible state storage)
    created_at: datetime
    updated_at: datetime
    is_archived: bool

    # Relationships
    sessions: List[Session]
    npcs: List[NPC]
    locations: List[Location]
    plot_threads: List[PlotThread]
```

#### Sessions (Chat Sessions)
```python
class Session(Base):
    id: UUID (primary key)
    campaign_id: UUID (foreign key → Campaigns)
    title: str (auto-generated or user-provided)
    session_number: int
    use_prompt_enhancement: bool
    created_at: datetime
    updated_at: datetime

    # Relationships
    messages: List[Message]
```

#### Messages
```python
class Message(Base):
    id: UUID (primary key)
    session_id: UUID (foreign key → Sessions)
    role: str ("user" | "assistant")
    content: str
    tokens: int
    metadata: JSONB (agent processing info)
    created_at: datetime
```

#### NPCs
```python
class NPC(Base):
    id: UUID (primary key)
    campaign_id: UUID (foreign key → Campaigns)
    name: str (indexed)
    type: str ("pc" | "npc" | "creature")
    role: str (occupation/archetype)
    narrative_data: JSONB ({
        traits: List[str],
        location: str,
        status: str,
        relationships: List[Dict],
        notes: List[str]
    })
    mechanics_data: JSONB ({
        race: str,
        classes: List[Dict],
        stats: Dict,
        equipment: Dict
    })
    searchable_text: str (generated, indexed for fuzzy search)
    created_at: datetime
    updated_at: datetime
```

#### Locations (Places)
```python
class Location(Base):
    id: UUID (primary key)
    campaign_id: UUID (foreign key → Campaigns)
    name: str (indexed)
    category: str ("city", "dungeon", "building", etc.)
    location_data: JSONB ({
        description: str,
        state: str,
        features: List[str],
        connections: List[Dict],
        occupants: List[str],
        secrets: str
    })
    searchable_text: str (generated, indexed)
    created_at: datetime
    updated_at: datetime
```

#### Items
```python
class Item(Base):
    id: UUID (primary key)
    campaign_id: UUID (foreign key → Campaigns)
    name: str (indexed)
    category: str ("weapon", "artifact", "document", etc.)
    item_data: JSONB ({
        description: str,
        features: List[str],
        connections: List[Dict],
        history: List[str],
        secrets: str
    })
    searchable_text: str (generated, indexed)
    created_at: datetime
    updated_at: datetime
```

#### PlotThreads
```python
class PlotThread(Base):
    id: UUID (primary key)
    campaign_id: UUID (foreign key → Campaigns)
    title: str
    description: str
    priority: str ("high" | "medium" | "low")
    status: str ("active" | "dormant" | "resolved")
    thread_data: JSONB ({
        involved_npcs: List[UUID],
        next_steps: List[str],
        notes: List[str]
    })
    created_session_id: UUID
    last_active_session_id: UUID
    created_at: datetime
    updated_at: datetime
```

## API Endpoints

### Authentication
```
POST   /api/auth/register        - Create new user account
POST   /api/auth/login           - Login and receive JWT token
POST   /api/auth/logout          - Invalidate token
GET    /api/auth/me              - Get current user info
PATCH  /api/auth/me              - Update user preferences
```

### Campaigns
```
GET    /api/campaigns            - List user's campaigns
POST   /api/campaigns            - Create new campaign
GET    /api/campaigns/{id}       - Get campaign details
PATCH  /api/campaigns/{id}       - Update campaign
DELETE /api/campaigns/{id}       - Delete campaign
GET    /api/campaigns/{id}/export - Export campaign data
```

### Sessions (Chats)
```
GET    /api/campaigns/{id}/sessions        - List campaign sessions
POST   /api/campaigns/{id}/sessions        - Create new session
GET    /api/sessions/{id}                  - Get session with messages
PATCH  /api/sessions/{id}                  - Update session (e.g., title)
DELETE /api/sessions/{id}                  - Delete session
```

### Messages
```
POST   /api/sessions/{id}/messages         - Send message (SSE streaming response)
GET    /api/sessions/{id}/messages         - Get message history
```

### Entities (NPCs, Locations, Items)
```
GET    /api/campaigns/{id}/npcs            - List campaign NPCs
POST   /api/campaigns/{id}/npcs            - Create NPC
PATCH  /api/npcs/{id}                      - Update NPC
DELETE /api/npcs/{id}                      - Delete NPC

GET    /api/campaigns/{id}/locations       - List campaign locations
POST   /api/campaigns/{id}/locations       - Create location
PATCH  /api/locations/{id}                 - Update location
DELETE /api/locations/{id}                 - Delete location

GET    /api/campaigns/{id}/items           - List campaign items
POST   /api/campaigns/{id}/items           - Create item
PATCH  /api/items/{id}                     - Update item
DELETE /api/items/{id}                     - Delete item
```

### Plot Threads
```
GET    /api/campaigns/{id}/plot-threads    - List plot threads
POST   /api/campaigns/{id}/plot-threads    - Create plot thread
PATCH  /api/plot-threads/{id}              - Update plot thread
DELETE /api/plot-threads/{id}              - Delete plot thread
```

## Feature Requirements

### Core Features (Phase 1)

#### 1. User Authentication & Account Management
- Email/password registration and login
- JWT-based authentication
- Password reset via email (future enhancement)
- User preferences (theme, default model, etc.)
- Secure API key storage (encrypted at rest)

#### 2. Campaign Management
- Create, edit, delete campaigns
- Campaign browser with search/filter
- Archive old campaigns
- Campaign dashboard showing recent activity
- Quick campaign switching

#### 3. Enhanced Chat Interface
- Real-time streaming AI responses (SSE)
- Markdown rendering for formatted text
- Campaign context awareness
- Message history with infinite scroll
- Copy/edit/regenerate message actions
- Visual distinction between user and AI messages

#### 4. Prompt Enhancement Pipeline (PEP)
- **Entity Agent**: Extract and match characters, places, items
- **Context Agent**: Maintain conversation continuity
- Toggle enhancement on/off per session
- Processing indicators during enhancement
- Agent metadata in message storage

#### 5. Entity Management
- CRUD operations for NPCs, locations, items
- Rich entity detail views
- Search and filter entities
- Fuzzy search matching during PEP
- Auto-extraction of entities from conversations (future)

#### 6. Agent System Architecture
- **Entity Agent**: Python port of existing JS implementation
  - Extract entities from user prompts
  - Fuzzy match against campaign database
  - Generate contextual enhancements
- **Mechanics Agent**: Analyze player actions for mechanical triggers
- **Antagonist Agent**: Ensure NPCs act according to motivations
- **Continuity Agent**: Maintain consistency with established facts

### Advanced Features (Phase 2)

#### 7. Multi-User Collaboration (Future)
- Share campaigns with other users
- Role-based permissions (GM, Player, Viewer)
- Real-time collaborative sessions
- Player character sheets managed by users

#### 8. Campaign Tools
- Session summaries and timelines
- Plot thread tracking and management
- World-building templates
- Random generators (names, events, complications)

#### 9. Mechanical Integration
- System-specific rule sets (D&D 5e, Pathfinder, etc.)
- Dice roller integration
- Combat tracker
- Character sheet storage

#### 10. Advanced AI Features
- Custom agent configuration per campaign
- Adjustable AI personality/tone
- Campaign-specific prompts and instructions
- Multi-model support (different Claude versions)

## User Experience Flow

### New User Onboarding
1. User visits website, sees landing page
2. User registers with email/password
3. User enters Claude API key (with explanation and link)
4. User creates first campaign
5. User starts first session with guided tutorial

### Campaign Setup
1. User clicks "New Campaign" button
2. Modal shows campaign creation form:
   - Title (required)
   - RPG System (dropdown)
   - Description (optional)
3. Campaign created, redirected to campaign page
4. User can add NPCs, locations, items manually or start chatting

### Session Play
1. User selects campaign from dashboard
2. User clicks "New Session" or continues existing session
3. Chat interface loads with campaign context
4. User types message, clicks send
5. **Agent Processing Pipeline** (if enhancement enabled):
   - Frontend shows "processing" indicator
   - Backend extracts entities via Entity Agent
   - Backend enriches prompt with campaign context
   - Backend sends enhanced prompt to Claude API
   - Backend streams response via SSE
   - Frontend renders streaming text in real-time
6. Message saved to database
7. User continues conversation

### Entity Management
1. User navigates to "Entities" tab in campaign view
2. User sees tabs for NPCs, Locations, Items
3. User clicks "Add NPC" button
4. Modal shows NPC creation form with YAML preview
5. User fills in narrative and mechanical data
6. NPC saved to database with searchable text generated
7. NPC appears in entity list and is available for PEP matching

## Security & Privacy

### Authentication Security
- Passwords hashed with bcrypt (cost factor 12)
- JWT tokens with 24-hour expiration
- HTTP-only cookies (if using cookie auth)
- HTTPS enforced in production

### Data Security
- User API keys encrypted at rest (AES-256)
- Database credentials in environment variables
- SQL injection protection via ORM
- Input validation and sanitization

### Authorization
- Row-level security: Users only access their own data
- All endpoints require authentication
- Campaign ownership verified on every request
- No shared campaigns in Phase 1 (prevents access issues)

### Privacy
- No analytics or tracking in Phase 1
- User data not shared or sold
- Campaign data stored securely
- Option to delete account and all data

## Performance Considerations

### Backend Optimization
- Database connection pooling (SQLAlchemy)
- Indexed queries on user_id, campaign_id, searchable_text
- JSONB GIN indexes for entity searching
- Async/await for concurrent Claude API calls
- Response streaming to reduce perceived latency

### Frontend Optimization
- Lazy loading for entity lists
- Virtual scrolling for long message histories
- Code splitting via Vite
- Debounced search inputs
- Cached campaign data (Vue reactivity)

### Scalability
- Stateless API (horizontal scaling possible)
- Database optimized for reads (most common operation)
- Agent processing queue (if load increases)
- CDN for static frontend assets (Railway edge)

## Deployment Strategy

### Railway Configuration
```yaml
# railway.toml (backend)
[build]
builder = "NIXPACKS"
buildCommand = "pip install -r requirements.txt"

[deploy]
startCommand = "uvicorn app.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
restartPolicyType = "ON_FAILURE"

[[services]]
name = "chronicler-backend"
```

### Environment Variables
```
# Backend
DATABASE_URL=postgresql://...
SECRET_KEY=<random_secret>
ANTHROPIC_API_KEY=<default_key>  # Optional fallback
CORS_ORIGINS=https://chronicler.example.com
LOG_LEVEL=info

# Frontend (build time)
VITE_API_BASE_URL=https://api.chronicler.example.com
```

### Deployment Pipeline
1. Developer pushes to `main` branch
2. Railway detects change, triggers build
3. Backend: Installs dependencies, runs migrations, starts server
4. Frontend: Builds Vite production bundle, serves via CDN
5. Health check passes, new version goes live
6. Old version kept for instant rollback

### Database Migrations
- Alembic manages schema versions
- Migrations run automatically on deploy
- Rollback capability for failed migrations
- Backup before major schema changes

## Success Metrics

### Quantitative
- User registration conversion rate
- Average session duration
- Messages per session
- Campaign retention (users with 5+ sessions)
- API response times (p95 < 500ms)
- Entity extraction accuracy (>80%)

### Qualitative
- Players report feeling appropriately challenged
- Game world feels coherent and reactive
- AI demonstrates "memory" of previous events
- Seamless narrative and mechanical integration
- Users prefer this to standard AI chat for RPGs

## Technical Constraints

### Backend Constraints
- FastAPI async patterns required for streaming
- PostgreSQL JSONB for flexible entity storage
- SQLAlchemy ORM for type safety and migrations
- Python 3.11+ for performance and type hints

### Frontend Constraints
- Vue 3 Composition API (no Options API)
- No TypeScript (per requirement)
- Scoped styles to avoid CSS conflicts
- SSE for streaming (no WebSockets in Phase 1)

### Infrastructure Constraints
- Railway deployment (no AWS/GCP complexity)
- PostgreSQL as primary database (no Redis yet)
- Single-region deployment initially
- Vertical scaling before horizontal

## Future Expansion (Post-Phase 2)

### Technical Enhancements
- Redis caching layer for hot data
- WebSocket support for real-time collaboration
- Background job queue (Celery/RQ) for heavy processing
- Full-text search engine (Meilisearch) for chat history
- Object storage (S3) for images/maps/documents

### Feature Enhancements
- Mobile-optimized interface (responsive design+)
- Offline mode with service workers
- Campaign templates and starter packs
- Community marketplace for shared content
- Virtual tabletop integration (maps, tokens)
- Voice input/output for hands-free play
- AI image generation for NPCs/locations
- Advanced dice mechanics and probability calculators

### Business Model (Optional)
- Freemium: Free tier with message limits
- Premium: Unlimited messages + advanced features
- API key options: Use own key (free) or pay per message
- No ads, ever

## Success Criteria
The application succeeds when:

1. **Accessibility**: Users can access campaigns from any device, anywhere
2. **Challenge**: Players face meaningful obstacles and failures
3. **Consistency**: NPCs and world elements behave predictably based on established facts
4. **Integration**: Narrative and mechanical elements flow seamlessly together
5. **Engagement**: Players prefer this system to standard AI chat for RPG sessions
6. **Persistence**: Campaigns can run for dozens of sessions while maintaining coherence
7. **Performance**: Fast response times despite agent processing overhead
8. **Reliability**: 99%+ uptime, no data loss, robust error handling

## Development Phases

### Phase 0: Foundation (2-3 weeks)
- Backend API scaffolding (FastAPI + PostgreSQL)
- Authentication system
- Database schema and migrations
- Frontend scaffolding (Vue 3 + Vite)
- Basic routing and layout

### Phase 1: Core Features (4-6 weeks)
- Campaign CRUD operations
- Chat interface with streaming
- Entity Agent (ported from JS to Python)
- Entity management (NPCs, locations, items)
- PEP integration with chat flow

### Phase 2: Enhancement (3-4 weeks)
- Additional agents (Mechanics, Antagonist, Continuity)
- Plot thread management
- Advanced entity features
- Search and filtering
- Performance optimization

### Phase 3: Polish (2-3 weeks)
- UI/UX refinement
- Error handling and edge cases
- Testing and bug fixes
- Documentation
- Production deployment

**Total Timeline: 11-16 weeks (3-4 months)**

## Appendix: Technology Justification

### Why Python/FastAPI?
- **Agent complexity**: Python is better for complex NLP/AI logic than JavaScript
- **Async performance**: FastAPI rivals Node.js in benchmarks
- **Type hints**: Better code quality without TypeScript
- **Ecosystem**: Rich libraries for data processing, ML, etc.
- **Maintainability**: More readable, less verbose than JS for backend

### Why Vue 3?
- **Learning curve**: Easiest framework for vanilla JS developers
- **No TypeScript**: Works great with plain JS
- **Performance**: Fast, lightweight (20KB runtime)
- **Composition API**: Modern, clean, powerful
- **Community**: Large, helpful, well-documented

### Why PostgreSQL?
- **JSONB**: Flexible schema for game entities
- **Full-text search**: Built-in, no extra service needed
- **Relations**: Proper foreign keys and joins
- **Mature**: Rock-solid, well-understood
- **Railway support**: First-class integration

### Why Railway?
- **Simplicity**: Zero-config deployments
- **All-in-one**: Backend + database + frontend
- **Cost**: $5-10/month for indie dev
- **DX**: Best developer experience in hosting
- **Scaling**: Easy to upgrade as needs grow
/exit/