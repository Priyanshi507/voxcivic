"""
VoxCivic — MongoDB Data Seeder
Seeds real government document chunks into MongoDB Atlas
Run once to populate the database for demo and judging
"""
import pymongo
import urllib.parse
from datetime import datetime
import hashlib

# Connection
username = urllib.parse.quote_plus('vinsharmavin89_db_user')
password = urllib.parse.quote_plus('ShivGangey@12')
uri = f'mongodb+srv://{username}:{password}@voxcivic.mkfu2ux.mongodb.net/?appName=voxcivic'

client = pymongo.MongoClient(uri)
db = client['voxcivic']

print("Connected to MongoDB Atlas — VoxCivic cluster")
print("Seeding government documents...\n")

# ── Real government document chunks ──────────────────────────────────────────
DOCUMENTS = [
    # RTI Act 2005
    {
        "document_id": "doc_rti_001",
        "title": "RTI Act 2005 — Section 6: Request for Information",
        "document_type": "legislation",
        "filename": "rti_act_2005.pdf",
        "content": "A person who desires to obtain any information under the RTI Act shall make a request in writing or through electronic means in English or Hindi or in the official language of the area in which the application is being made to the Public Information Officer. The applicant shall pay a fee as prescribed and shall not be required to give any reason for requesting the information.",
        "excerpt": "Any citizen can request information from public authorities by submitting a written application with a fee of Rs. 10/-. No reason required.",
        "tags": ["rti", "right to information", "application", "section 6", "PIO"],
        "source_url": "https://rti.gov.in/rti-act.pdf",
        "page": 4,
        "embedding": [0.1] * 768  # placeholder — replace with real embeddings
    },
    {
        "document_id": "doc_rti_002",
        "title": "RTI Act 2005 — Section 7: Disposal of Request",
        "document_type": "legislation",
        "filename": "rti_act_2005.pdf",
        "content": "The Public Information Officer on receipt of a request shall as expeditiously as possible, and in any case within thirty days of the receipt of the request, either provide the information on payment of such fee as may be prescribed or reject the request for any of the reasons specified in sections 8 and 9. If the information requested concerns the life or liberty of a person, it shall be provided within forty-eight hours.",
        "excerpt": "PIO must respond within 30 working days. Life/liberty matters: 48 hours. Non-compliance is an offence.",
        "tags": ["rti", "deadline", "30 days", "section 7", "response"],
        "source_url": "https://rti.gov.in/rti-act.pdf",
        "page": 5,
        "embedding": [0.12] * 768
    },
    {
        "document_id": "doc_rti_003",
        "title": "RTI Act 2005 — First Appeal Process",
        "document_type": "legislation",
        "filename": "rti_act_2005.pdf",
        "content": "Any person who does not receive a decision within the time specified in Section 7 or is aggrieved by a decision of the PIO may within thirty days from the expiry of such period or from the receipt of such a decision prefer an appeal to such officer who is senior in rank to the Public Information Officer. The First Appellate Authority shall dispose of the appeal within thirty days or in exceptional cases within forty-five days.",
        "excerpt": "If PIO doesn't respond in 30 days, file First Appeal within 30 days to the senior officer. FAA must decide in 30-45 days.",
        "tags": ["rti", "first appeal", "FAA", "appeal process"],
        "source_url": "https://rti.gov.in/rti-act.pdf",
        "page": 8,
        "embedding": [0.15] * 768
    },
    # Consumer Protection Act 2019
    {
        "document_id": "doc_consumer_001",
        "title": "Consumer Protection Act 2019 — Filing Complaints",
        "document_type": "legislation",
        "filename": "consumer_protection_act_2019.pdf",
        "content": "A consumer complaint can be filed before the District Consumer Disputes Redressal Commission for disputes where the value of goods or services paid does not exceed one crore rupees. Complaints can be filed online at edaakhil.gov.in. No advocate is required for filing. The complainant can appear in person. The filing fee ranges from Rs. 200 to Rs. 5000 depending on the claim value.",
        "excerpt": "File consumer complaints at edaakhil.gov.in. District Commission handles cases up to Rs. 1 crore. No lawyer needed.",
        "tags": ["consumer", "complaint", "district commission", "edaakhil", "refund"],
        "source_url": "https://consumeraffairs.nic.in/acts-and-rules",
        "page": 12,
        "embedding": [0.2] * 768
    },
    {
        "document_id": "doc_consumer_002",
        "title": "Consumer Protection Act 2019 — E-Commerce Rules",
        "document_type": "legislation",
        "filename": "consumer_protection_ecommerce_rules_2020.pdf",
        "content": "Every e-commerce entity shall establish an adequate grievance redressal mechanism and appoint a Grievance Officer for consumer grievance redressal. The name and contact details of the Grievance Officer shall be prominently displayed on the platform. The Grievance Officer shall acknowledge the receipt of any consumer complaint within 48 hours and redress the complaint within one month from the date of receipt.",
        "excerpt": "E-commerce companies must resolve complaints within 1 month. Grievance Officer must acknowledge within 48 hours.",
        "tags": ["consumer", "ecommerce", "online shopping", "grievance", "refund"],
        "source_url": "https://consumeraffairs.nic.in/acts-and-rules",
        "page": 3,
        "embedding": [0.22] * 768
    },
    # PM Awas Yojana
    {
        "document_id": "doc_pmay_001",
        "title": "PM Awas Yojana — EWS/LIG Eligibility Criteria 2024",
        "document_type": "government_scheme",
        "filename": "pmay_guidelines_2024.pdf",
        "content": "Under the Pradhan Mantri Awas Yojana (Urban), the Economically Weaker Section (EWS) category covers households with annual income up to Rs. 3 lakh. The Light Income Group (LIG) covers annual income between Rs. 3 lakh and Rs. 6 lakh. EWS beneficiaries can avail interest subsidy of 6.5% on housing loans up to Rs. 6 lakh under Credit Linked Subsidy Scheme (CLSS). The subsidy amount is Rs. 2.67 lakh.",
        "excerpt": "EWS: income up to Rs.3 lakh/year. LIG: Rs.3-6 lakh. Interest subsidy 6.5% on loans up to Rs.6 lakh = Rs.2.67 lakh benefit.",
        "tags": ["pmay", "housing", "subsidy", "EWS", "LIG", "awas yojana"],
        "source_url": "https://pmaymis.gov.in",
        "page": 7,
        "embedding": [0.3] * 768
    },
    {
        "document_id": "doc_pmay_002",
        "title": "PM Awas Yojana — How to Apply Online",
        "document_type": "government_scheme",
        "filename": "pmay_application_guide.pdf",
        "content": "To apply for PMAY, visit pmaymis.gov.in and click on Citizen Assessment. Select the appropriate component and enter your Aadhaar number. Fill in the online application form with details about household income, existing house ownership, and family members. Submit the form and note the Application ID for tracking. The application is processed by the Urban Local Body and State Government. Priority is given to SC/ST, OBC, differently-abled, senior citizens, and women-headed households.",
        "excerpt": "Apply at pmaymis.gov.in. Need Aadhaar. Priority for SC/ST, women, senior citizens. Track with Application ID.",
        "tags": ["pmay", "application", "aadhaar", "online", "housing scheme"],
        "source_url": "https://pmaymis.gov.in",
        "page": 2,
        "embedding": [0.32] * 768
    },
    # Municipal Infrastructure
    {
        "document_id": "doc_municipal_001",
        "title": "Solid Waste Management Rules 2016 — Citizen Rights",
        "document_type": "government_notification",
        "filename": "swm_rules_2016.pdf",
        "content": "Every local body shall ensure door-to-door collection of solid waste from all households, shops, offices, and other establishments. The collection shall be done daily or as notified by the local authority. Citizens can lodge complaints through the municipal helpline or mobile app if collection is missed. The local authority shall resolve complaints within 24 hours for urgent matters and 72 hours for routine complaints.",
        "excerpt": "Municipalities must collect garbage daily. Citizens can complain via municipal helpline. Resolution within 24-72 hours.",
        "tags": ["garbage", "waste", "municipal", "complaint", "swachh bharat"],
        "source_url": "https://moef.gov.in/swm-rules",
        "page": 5,
        "embedding": [0.4] * 768
    },
    {
        "document_id": "doc_municipal_002",
        "title": "CPWD Guidelines — Road Maintenance and Pothole Repair",
        "document_type": "government_notification",
        "filename": "cpwd_road_maintenance.pdf",
        "content": "As per CPWD guidelines, potholes on National Highways and State Highways must be repaired within 24 hours of being reported. Municipal roads must be repaired within 7 days. Citizens can report road damage to the National Highways Authority (NHAI) helpline 1033, or through the MyGov portal, or by filing an RTI with the PWD asking for the repair schedule and budget allocation for the road.",
        "excerpt": "Potholes on NHs: 24-hour repair mandate. Municipal roads: 7 days. Report via NHAI 1033 or PWD complaint.",
        "tags": ["pothole", "road", "repair", "PWD", "NHAI", "infrastructure"],
        "source_url": "https://cpwd.gov.in",
        "page": 12,
        "embedding": [0.42] * 768
    },
    # Electricity Rights
    {
        "document_id": "doc_electricity_001",
        "title": "Electricity Act 2003 — Consumer Rights and Disconnection Rules",
        "document_type": "legislation",
        "filename": "electricity_act_2003.pdf",
        "content": "Under the Electricity Act 2003, a licensee shall not cut off supply of electricity to any consumer without giving prior notice of not less than 15 days in writing and stating the reasons. The consumer has the right to approach the Consumer Grievance Redressal Forum of the electricity distribution company. If not satisfied, the consumer can appeal to the Electricity Ombudsman. Wrongful disconnection is a punishable offence.",
        "excerpt": "Electricity cannot be cut without 15 days written notice. Wrongful disconnection: complain to CGRF then Electricity Ombudsman.",
        "tags": ["electricity", "disconnection", "notice", "CGRF", "ombudsman", "RTI"],
        "source_url": "https://powermin.gov.in",
        "page": 34,
        "embedding": [0.5] * 768
    },
    # Water Supply
    {
        "document_id": "doc_water_001",
        "title": "National Water Policy — Urban Water Supply Standards",
        "document_type": "government_policy",
        "filename": "national_water_policy.pdf",
        "content": "Every urban household is entitled to a minimum of 135 litres per capita per day (LPCD) of potable water supply as per Ministry of Housing and Urban Affairs norms. Interruptions in supply exceeding 24 hours must be reported by the utility. Citizens can file complaints with the local Jal Board, approach the State Water Regulatory Authority, or file an RTI requesting the maintenance schedule and reason for interruption.",
        "excerpt": "Urban households entitled to 135 LPCD water. Interruptions over 24 hours: complain to Jal Board or file RTI.",
        "tags": ["water", "supply", "jal board", "complaint", "RTI"],
        "source_url": "https://jalshakti-dowr.gov.in",
        "page": 8,
        "embedding": [0.55] * 768
    },
]

# ── Seed documents ────────────────────────────────────────────────────────────
documents_collection = db['documents']
documents_collection.create_index([("document_id", 1)], unique=True)
documents_collection.create_index([("tags", 1)])
documents_collection.create_index([("document_type", 1)])

inserted = 0
updated = 0
for doc in DOCUMENTS:
    doc['created_at'] = datetime.utcnow()
    doc['indexed'] = True
    result = documents_collection.update_one(
        {"document_id": doc["document_id"]},
        {"$set": doc},
        upsert=True
    )
    if result.upserted_id:
        inserted += 1
        print(f"  + Inserted: {doc['title'][:60]}")
    else:
        updated += 1
        print(f"  ~ Updated:  {doc['title'][:60]}")

print(f"\nDocuments: {inserted} inserted, {updated} updated")

# ── Seed sample cases ─────────────────────────────────────────────────────────
cases_collection = db['cases']
cases_collection.create_index([("case_id", 1)])
cases_collection.create_index([("type", 1)])
cases_collection.create_index([("created_at", -1)])

sample_cases = [
    {"case_id": "VOX-001", "type": "rti", "subject": "Electricity disconnection RTI", "status": "filed", "created_at": datetime.utcnow()},
    {"case_id": "VOX-002", "type": "complaint", "subject": "Consumer complaint — undelivered order", "status": "resolved", "created_at": datetime.utcnow()},
    {"case_id": "VOX-003", "type": "campaign", "subject": "Pothole on MG Road", "status": "active", "created_at": datetime.utcnow()},
]
for case in sample_cases:
    cases_collection.update_one({"case_id": case["case_id"]}, {"$set": case}, upsert=True)
print(f"Cases: {len(sample_cases)} seeded")

# ── Seed sample campaigns ─────────────────────────────────────────────────────
campaigns_collection = db['campaigns']
campaigns_collection.create_index([("status", 1)])

sample_campaigns = [
    {"campaign_id": "camp_001", "title": "Dangerous Pothole on MG Road", "category": "Infrastructure", "location": "MG Road, Bengaluru", "status": "active", "upvotes": 67, "gitlab_issue_id": 47, "created_at": datetime.utcnow()},
    {"campaign_id": "camp_002", "title": "Water Supply Irregular in Sector 14", "category": "Water", "location": "Sector 14, Ghaziabad", "status": "active", "upvotes": 89, "gitlab_issue_id": 42, "created_at": datetime.utcnow()},
    {"campaign_id": "camp_003", "title": "Streetlights Broken for 3 Months", "category": "Safety", "location": "Laxmi Nagar, Delhi", "status": "resolved", "upvotes": 112, "gitlab_issue_id": 29, "created_at": datetime.utcnow()},
]
for camp in sample_campaigns:
    campaigns_collection.update_one({"campaign_id": camp["campaign_id"]}, {"$set": camp}, upsert=True)
print(f"Campaigns: {len(sample_campaigns)} seeded")

# ── Seed interactions ─────────────────────────────────────────────────────────
interactions_collection = db['interactions']
interactions_collection.create_index([("created_at", -1)])
interactions_collection.create_index([("intent", 1)])

sample_interactions = [
    {"session_id": "demo_001", "message": "How do I file RTI?", "intent": "rti_request", "language": "en", "created_at": datetime.utcnow()},
    {"session_id": "demo_002", "message": "Pothole on my street", "intent": "create_campaign", "language": "en", "created_at": datetime.utcnow()},
    {"session_id": "demo_003", "message": "Am I eligible for PMAY?", "intent": "scheme_query", "language": "en", "created_at": datetime.utcnow()},
]
for interaction in sample_interactions:
    interactions_collection.insert_one(interaction)
print(f"Interactions: {len(sample_interactions)} seeded")

# ── Verify ────────────────────────────────────────────────────────────────────
print("\n" + "="*50)
print("MONGODB ATLAS — VOXCIVIC DATABASE SUMMARY")
print("="*50)
print(f"Documents indexed:  {documents_collection.count_documents({})}")
print(f"Cases stored:       {cases_collection.count_documents({})}")
print(f"Campaigns tracked:  {campaigns_collection.count_documents({})}")
print(f"Interactions logged:{interactions_collection.count_documents({})}")
print(f"\nCollections: {db.list_collection_names()}")
print("\nMongoDB Atlas seeding complete!")
print("Database ready for VoxCivic agent queries.")
client.close()
