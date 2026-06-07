# VoxCivic — AI Civic Empowerment Agent

> **Google Cloud Rapid Agent Hackathon 2026 · MongoDB Partner Track**

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Gemini 2.5](https://img.shields.io/badge/Gemini-2.5%20Flash-blue)](https://ai.google.dev)
[![MongoDB Atlas](https://img.shields.io/badge/MongoDB-Atlas%20Vector%20Search-green)](https://mongodb.com/atlas)
[![GitLab MCP](https://img.shields.io/badge/GitLab-MCP%20Integration-orange)](https://gitlab.com)
[![Live Demo](https://img.shields.io/badge/Live-voxcivic.onrender.com-brightgreen)](https://voxcivic.onrender.com)

---

## The Problem — 1.4 Billion People. Locked Out of Their Own Government.

Every year, millions of citizens face illegal electricity disconnections, unresponsive municipalities, denied housing benefits, and consumer fraud — with no idea how to fight back. Filing an RTI (Right to Information) request — a constitutional right in India — requires navigating complex legal language, bureaucratic procedures, and 30-day deadlines that most citizens don't know exist.

**Less than 2% of eligible citizens ever file an RTI. Complexity is the barrier.**

VoxCivic removes that barrier entirely.

---

## The Solution — Your Personal AI Civic Advocate

VoxCivic is a multi-tool AI agent that empowers any citizen to:

- **Ask questions** about government policies, schemes, and their rights in plain language
- **Generate legally formatted RTI requests** in under 2 minutes — ready to file
- **Report and track civic issues** (potholes, water supply, garbage) via GitLab campaigns
- **Find government schemes** they qualify for (PMAY, Jan Dhan, Ayushman Bharat)
- **File consumer complaints** with the correct legal format and filing guidance

**Built with Gemini 2.5 Flash + MongoDB Atlas Vector Search + GitLab MCP**

---

## Live Demo

**Frontend:** https://voxcivic.onrender.com  
**API:** https://voxcivic-api.onrender.com  
**API Docs:** https://voxcivic-api.onrender.com/api/docs

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   VoxCivic Frontend                  │
│              HTML/CSS/JS — Render Static             │
│   Chat UI · RTI Generator · Campaign Tracker        │
│                 Dashboard · Documents                │
└─────────────────────┬───────────────────────────────┘
                      │ HTTPS REST API
┌─────────────────────▼───────────────────────────────┐
│              VoxCivic Agent Backend                  │
│              Python FastAPI — Render                 │
│                                                      │
│  ┌──────────────────────────────────────────────┐   │
│  │           Gemini 2.5 Flash                   │   │
│  │    Google AI — Generative Language API       │   │
│  │  Multi-turn reasoning · Intent detection     │   │
│  │  RTI generation · Civic guidance             │   │
│  └──────────────────────────────────────────────┘   │
│                                                      │
│  ┌─────────────────┐   ┌──────────────────────┐     │
│  │  MongoDB Atlas  │   │    GitLab MCP        │     │
│  │  Vector Search  │   │  Issue Tracking      │     │
│  │  Partner: MCP   │   │  Campaign Manager    │     │
│  └─────────────────┘   └──────────────────────┘     │
└─────────────────────────────────────────────────────┘
         │                          │
┌────────▼────────┐      ┌─────────▼────────┐
│  MongoDB Atlas  │      │   GitLab Cloud   │
│  Mumbai Region  │      │  Public Issues   │
│  M0 Free Tier   │      │  voxcivic-camp.. │
│  Vector Index   │      │  Community votes │
└─────────────────┘      └──────────────────┘
```

---

## Google Cloud Integration

VoxCivic uses **Google's Generative Language API (Gemini 2.5 Flash)** as the core reasoning engine:

- **Model:** `gemini-2.5-flash` via `generativelanguage.googleapis.com`
- **Capability used:** Multi-turn reasoning, intent classification, document generation
- **Why Gemini 2.5 Flash:** Fastest response time for citizen queries, superior instruction-following for legal document generation, multilingual support (English + Hindi)

Every citizen message goes through a multi-step Gemini reasoning pipeline:
1. Intent detection (RTI / civic issue / scheme / consumer complaint)
2. Context retrieval from MongoDB Vector Search
3. Response generation with specific steps, portals, fees, deadlines
4. Suggested follow-up actions

---

## MongoDB Partner Integration

VoxCivic uses **MongoDB Atlas** as the primary data layer with three collections:

### 1. Vector Search — Semantic Document Retrieval
Government documents (RTI Act, Consumer Protection Act, PMAY guidelines) are chunked and embedded. When a citizen asks a question, MongoDB Atlas Vector Search finds the most semantically relevant document chunks:

```python
pipeline = [
    {
        "$vectorSearch": {
            "index": "document_vector_index",
            "path": "embedding",
            "queryVector": query_embedding,  # from Vertex AI text-embedding-004
            "numCandidates": 50,
            "limit": 4
        }
    },
    {
        "$project": {
            "title": 1, "excerpt": 1, "document_id": 1,
            "score": {"$meta": "vectorSearchScore"}
        }
    }
]
```

### 2. Case Management — Persistent Agent Memory
Every citizen interaction is stored as a case in MongoDB, enabling:
- Full conversation history across sessions
- RTI letter tracking (filed / pending / resolved)
- Campaign status updates

### 3. Analytics Aggregation
Real-time civic engagement analytics via MongoDB aggregation pipelines — total questions answered, top issue categories, resolution rates.

**Atlas Vector Search Index Configuration:**
```json
{
  "fields": [{
    "type": "vector",
    "path": "embedding",
    "numDimensions": 768,
    "similarity": "cosine"
  }]
}
```

**MongoDB Cluster:** `voxcivic.mkfu2ux.mongodb.net` (Mumbai, ap-south-1)

---

## GitLab MCP Integration

When a citizen reports a civic issue, VoxCivic automatically creates a **GitLab issue** for public tracking:

- Issue title, description, and labels auto-generated by Gemini
- Community can upvote and comment to show support
- Status tracked: Draft → Active → Under Review → Resolved
- Milestone tracking for resolution deadlines

This creates a **transparent, public record** of civic issues — accountability through visibility.

---

## Key Features

| Feature | Technology | Description |
|---|---|---|
| AI Chat Agent | Gemini 2.5 Flash | Multi-turn civic guidance in English & Hindi |
| Document Q&A | MongoDB Vector Search | Semantic search across 147 government documents |
| RTI Generator | Gemini + Template Engine | Legally formatted RTI letters in 2 minutes |
| Campaign Tracker | GitLab MCP | Public issue tracking with community votes |
| Analytics Dashboard | MongoDB Aggregations | Real-time civic engagement metrics |
| Consumer Complaints | Gemini reasoning | Step-by-step guidance for consumer forums |
| Scheme Eligibility | Document retrieval | PMAY, Jan Dhan, Ayushman Bharat eligibility checks |

---

## Impact Potential

| Metric | Data |
|---|---|
| Target population | 1.4 billion Indian citizens |
| RTI eligibility | Every Indian citizen (constitutional right) |
| Current RTI filing rate | < 2% of eligible citizens |
| Civic issues reported annually | 50+ million unresolved complaints |
| Consumer complaints filed | 5M+ annually, majority unresolved |
| Government schemes unclaimed | ₹50,000+ crore in unclaimed benefits yearly |

VoxCivic's architecture is replicable in **any democracy** with freedom of information laws — USA (FOIA), UK (Freedom of Information Act), EU member states, Australia — making the global addressable population over 2 billion citizens.

---

## Quick Start

### Prerequisites
- Python 3.11+
- MongoDB Atlas account (free M0 tier)
- Gemini API key (Google AI Studio)
- GitLab account + personal access token

### Setup

```bash
git clone https://github.com/Priyanshi507/voxcivic
cd voxcivic

# Backend
cd backend
pip install -r requirements.txt

# Set environment variables
export GEMINI_API_KEY=your_gemini_key
export MONGODB_URI=your_mongodb_uri
export GITLAB_TOKEN=your_gitlab_token

# Run
uvicorn main:app --reload --port 8000
```

### Frontend
Open `frontend/index.html` in any browser, or serve with:
```bash
cd frontend
python -m http.server 3000
```

---

## Project Structure

```
voxcivic/
├── backend/
│   ├── main.py              # FastAPI agent — Gemini + MongoDB + GitLab
│   └── requirements.txt     # Python dependencies
├── frontend/
│   └── index.html           # Complete single-file React-style UI
├── .gitignore
├── README.md
└── LICENSE                  # MIT License
```

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/chat` | Main agent chat — Gemini reasoning |
| POST | `/api/rti` | Generate RTI letter |
| GET/POST | `/api/campaigns` | List / create GitLab campaigns |
| GET | `/api/analytics` | MongoDB aggregated metrics |
| GET | `/api/health` | Service health check |

---

## Judging Criteria Alignment

**Technological Implementation**
Gemini 2.5 Flash for multi-step reasoning, MongoDB Atlas Vector Search for semantic document retrieval, GitLab MCP for campaign tracking, FastAPI for production-grade REST API, deployed on Render with environment-based configuration.

**Design**
Clean light-theme UI with DM Serif Display typography, warm cream/sand color system, responsive layout, real-time agent status indicators, suggested action chips, source attribution on every response.

**Potential Impact**
Addresses civic access gap for 1.4B+ citizens. Reduces RTI filing barrier from hours to 2 minutes. Creates transparent public record of unresolved civic issues. Replicable globally in any democracy.

**Quality of Idea**
No other team will build civic empowerment infrastructure. VoxCivic sits at the intersection of AI, constitutional rights, and community organizing — a category-defining application that could become India's first AI-powered civic rights platform.

---

## Technologies Used

- **Google Gemini 2.5 Flash** — Core AI reasoning engine
- **MongoDB Atlas** — Vector Search + document store + analytics
- **GitLab API** — MCP integration for campaign issue tracking
- **FastAPI** — Production Python REST API framework
- **Render** — Cloud deployment (backend + frontend)

---

## Team

Built for the Google Cloud Rapid Agent Hackathon 2026.

---

## License

MIT License — see [LICENSE](LICENSE) for details.

This project was created during the Google Cloud Rapid Agent Hackathon contest period (May 5 – June 11, 2026).
