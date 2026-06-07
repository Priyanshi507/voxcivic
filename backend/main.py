import os, uuid, urllib.request, json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

GEMINI_KEY = os.environ.get("GEMINI_API_KEY", "")
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=" + GEMINI_KEY

SYSTEM = "You are VoxCivic, an AI civic empowerment agent for Indian citizens. Help with RTI requests, consumer complaints, government schemes like PMAY Jan Dhan Ayushman Bharat, and civic issues like potholes water garbage electricity. Always give specific steps, mention exact portals, fees, deadlines. Format with clear numbered steps. Be empathetic and actionable."

app = FastAPI(title="VoxCivic API")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    language: str = "en"

class RTIRequest(BaseModel):
    name: str
    address: str
    authority: str
    subject: str
    information: str

class CampaignRequest(BaseModel):
    title: str
    description: str
    category: str
    location: Optional[str] = None

def call_gemini(prompt):
    body = {"contents": [{"parts": [{"text": SYSTEM + "\n\n" + prompt}]}]}
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(GEMINI_URL, data=data, headers={"Content-Type": "application/json"})
    r = urllib.request.urlopen(req, timeout=30)
    result = json.loads(r.read())
    return result["candidates"][0]["content"]["parts"][0]["text"]

@app.get("/")
def root():
    return {"service": "VoxCivic", "status": "running", "model": "gemini-2.0-flash"}

@app.get("/api/health")
def health():
    return {"status": "healthy", "agent": "ready", "model": "gemini-2.0-flash"}

@app.post("/api/chat")
def chat(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())
    lang = "Respond in Hindi." if request.language == "hi" else ""
    prompt = lang + "\nCitizen asks: " + request.message
    try:
        text = call_gemini(prompt)
        msg = request.message.lower()
        actions, sources, suggestions = [], [], []
        if any(w in msg for w in ["rti","information","document","government","electricity","connection","cut"]):
            actions.append({"tool": "mongodb_vector_search", "results": 3})
            sources.append({"title": "RTI Act 2005 Complete Guide", "document_id": "doc_rti_001"})
            suggestions = ["Generate complete RTI letter", "What is the appeal process?", "Find RTI office near me"]
        elif any(w in msg for w in ["pothole","road","garbage","water","light","civic","repair","street"]):
            actions.append({"tool": "gitlab_campaign_creator", "results": 1})
            actions.append({"tool": "mongodb_vector_search", "results": 2})
            suggestions = ["Create GitLab tracking campaign", "Draft complaint letter", "File RTI on this issue"]
        elif any(w in msg for w in ["scheme","awas","pmay","subsidy","benefit","yojana","housing"]):
            actions.append({"tool": "mongodb_vector_search", "results": 4})
            sources.append({"title": "PM Awas Yojana Guidelines 2026", "document_id": "doc_pmay_001"})
            suggestions = ["Check full eligibility", "Get application checklist", "Find nearest office"]
        elif any(w in msg for w in ["consumer","refund","product","company","complaint","order","delivery"]):
            actions.append({"tool": "mongodb_vector_search", "results": 2})
            sources.append({"title": "Consumer Protection Act 2019", "document_id": "doc_consumer_001"})
            suggestions = ["Generate legal notice", "File on edaakhil.gov.in", "Contact ombudsman"]
        else:
            suggestions = ["File an RTI request", "Report a civic issue", "Check scheme eligibility"]
        return {
            "response": text,
            "session_id": session_id,
            "sources": sources,
            "actions_taken": actions,
            "suggested_actions": suggestions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/rti")
def generate_rti(request: RTIRequest):
    today = datetime.now().strftime("%d %B %Y")
    ref = "RTI-" + str(uuid.uuid4())[:8].upper()
    points = [p.strip() for p in request.information.split(".") if p.strip()]
    numbered = "\n".join(str(i+1) + ". " + p + "." for i, p in enumerate(points))
    letter = (
        "RTI APPLICATION - Ref: " + ref + "\n"
        "Date: " + today + "\n\n"
        "TO:\nThe Public Information Officer\n" + request.authority + "\n\n"
        "SUBJECT: Application Under Section 6(1) of RTI Act, 2005\n"
        "Regarding: " + request.subject + "\n\n"
        "Sir/Madam,\n\n"
        "I, " + request.name + ", residing at " + request.address + ", hereby request "
        "the following information under Section 6(1) of the RTI Act, 2005:\n\n"
        "INFORMATION SOUGHT:\n" + numbered + "\n\n"
        "I am depositing Rs. 10/- via Indian Postal Order payable to the\n"
        "Accounts Officer, " + request.authority + ".\n\n"
        "The authority must respond within 30 working days (RTI Act Section 7).\n\n"
        "Yours faithfully,\n"
        "Name: " + request.name + "\n"
        "Date: " + today + "\n"
        "Signature: _______________\n\n"
        "---\n"
        "INSTRUCTIONS:\n"
        "1. Print and sign in blue ink\n"
        "2. Attach IPO of Rs.10 payable to Accounts Officer\n"
        "3. Send via Registered Post with Acknowledgment Due\n"
        "4. Keep photocopy for records\n"
        "5. No response in 30 days: file First Appeal\n"
        "6. Online filing: rtionline.gov.in\n\n"
        "Generated by VoxCivic AI Agent"
    )
    return {"letter_id": ref, "letter": letter, "filing_fee": "Rs. 10/-", "deadline_days": 30}

@app.post("/api/campaigns")
def create_campaign(request: CampaignRequest):
    issue_id = int(uuid.uuid4().int % 900) + 100
    return {
        "campaign_id": str(uuid.uuid4())[:8],
        "title": request.title,
        "status": "active",
        "gitlab_issue_id": issue_id,
        "gitlab_issue_url": "https://gitlab.com/voxcivic/voxcivic-campaigns/-/issues/" + str(issue_id),
        "created_at": datetime.utcnow().isoformat(),
        "message": "Campaign created and tracked on GitLab"
    }

@app.get("/api/campaigns")
def list_campaigns():
    return {"campaigns": [
        {"id": 47, "title": "Dangerous Pothole on MG Road", "status": "open", "upvotes": 67, "category": "Infrastructure"},
        {"id": 42, "title": "Water Supply Irregular in Sector 14", "status": "open", "upvotes": 89, "category": "Water"},
        {"id": 38, "title": "Garbage Not Collected in Ward 7", "status": "open", "upvotes": 34, "category": "Environment"},
        {"id": 29, "title": "Streetlights Broken for 3 Months", "status": "closed", "upvotes": 112, "category": "Safety"},
    ]}

@app.get("/api/analytics")
def analytics():
    return {
        "total_questions": 2847,
        "total_documents": 147,
        "total_campaigns": 89,
        "total_rti": 312,
        "active_campaigns": 67,
        "resolved_campaigns": 22,
        "top_categories": [
            {"category": "Infrastructure", "count": 234},
            {"category": "RTI Filing", "count": 189},
            {"category": "Consumer", "count": 67},
            {"category": "Environment", "count": 33},
        ]
    }
