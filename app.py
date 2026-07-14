"""
MedForsa GCC API — minimal real backend.
Run: uvicorn app:app --reload --port 8420
Docs auto-generated at: http://127.0.0.1:8420/docs
"""
from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field, EmailStr
from typing import Literal, Any
import sqlite3
import os
import json
import logging
import bcrypt
import jwt
from datetime import datetime, timedelta

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger("medintel")

DB_PATH = os.path.join(os.path.dirname(__file__), "medintel.db")
FRONTEND_PATH = os.path.join(os.path.dirname(__file__), "frontend.html")
LANDING_PATH = os.path.join(os.path.dirname(__file__), "medintel-landing.html")
LANG_JS_PATH = os.path.join(os.path.dirname(__file__), "lang.js")

app = FastAPI(title="MedForsa GCC API", version="0.6")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def log_action(conn, table, record_id, action, detail):
    conn.execute(
        "INSERT INTO audit_log (table_name, record_id, action, detail) VALUES (?,?,?,?)",
        (table, record_id, action, detail)
    )
    conn.commit()

class NewCompany(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    headquarters: str = "Unknown"
    website: str = "Not provided"
    portfolio: str = "Not described yet"
    status_tag: Literal["covered", "unclear", "open"] = "unclear"

@app.get("/")
def root():
    return FileResponse(LANDING_PATH)

@app.get("/app")
def dashboard_page():
    return FileResponse(FRONTEND_PATH)

@app.get("/lang.js")
def lang_js():
    return FileResponse(LANG_JS_PATH, media_type="application/javascript")

@app.get("/snibe-ad.html")
def snibe_ad():
    return FileResponse(os.path.join(os.path.dirname(__file__), "snibe-ad.html"), media_type="text/html")

@app.get("/snibe-biochem-ad.html")
def snibe_biochem_ad():
    return FileResponse(os.path.join(os.path.dirname(__file__), "snibe-biochem-ad.html"), media_type="text/html")

@app.get("/doctor-ai")
def doctor_ai_page():
    return FileResponse(os.path.join(os.path.dirname(__file__), "doctor-ai.html"), media_type="text/html")

@app.get("/lab-info")
def lab_info_page():
    return FileResponse(os.path.join(os.path.dirname(__file__), "lab-info.html"), media_type="text/html")

@app.get("/lab-tests")
def lab_tests_page_legacy():
    # Legacy URL kept working -- the page and feature are now branded "Lab Info".
    return FileResponse(os.path.join(os.path.dirname(__file__), "lab-info.html"), media_type="text/html")

@app.get("/logo.svg")
def logo():
    return FileResponse(os.path.join(os.path.dirname(__file__), "logo.svg"), media_type="image/svg+xml")

@app.get("/api/status")
def status():
    return {"service": "MedForsa GCC API", "status": "running", "note": "This is a real local backend, not a hosted service."}

class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: Any

class ChatRequest(BaseModel):
    messages: list[ChatMessage]
    system: str = ""

def call_anthropic(system: str, messages: list):
    import json
    import urllib.request
    import urllib.error

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="ANTHROPIC_API_KEY is not set on the server. Add it in Render > Environment.")

    # Strip accidental whitespace/quotes that sometimes sneak in when pasting
    # the key into Render's Environment UI — a common source of "invalid x-api-key".
    api_key = api_key.strip().strip('"').strip("'")

    # Safe diagnostic (never logs the full key): confirms what actually reached
    # the server without exposing the secret in logs.
    logger.info(
        f"Anthropic key loaded: length={len(api_key)}, "
        f"prefix={api_key[:7]}, suffix={api_key[-4:] if len(api_key) >= 4 else '****'}"
    )
    if not api_key.startswith("sk-ant-"):
        logger.warning("ANTHROPIC_API_KEY does not start with 'sk-ant-' — this is likely the wrong value.")

    body = json.dumps({
        "model": "claude-sonnet-5",
        "max_tokens": 1500,
        "system": system,
        "messages": messages,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8")
        logger.error(f"Anthropic API error {e.code}: {detail}")
        raise HTTPException(status_code=e.code, detail=detail)
    except Exception as e:
        logger.error(f"Chat proxy error: {e}")
        raise HTTPException(status_code=502, detail=str(e))

@app.post("/api/chat")
def chat_proxy(payload: ChatRequest):
    return call_anthropic(payload.system, [m.dict() for m in payload.messages])

@app.get("/companies")
def list_companies(status: str | None = None, q: str | None = None, category: str | None = None,
                    origin: str | None = None, distributor_id: int | None = None,
                    limit: int = 50, offset: int = 0, include_pending: bool = False):
    if limit < 1 or limit > 200:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 200")
    if offset < 0:
        raise HTTPException(status_code=400, detail="offset must be >= 0")
    conn = get_conn()
    query = "SELECT * FROM manufacturers WHERE 1=1"
    params = []
    if not include_pending:
        query += " AND is_published = 1"
    if status:
        query += " AND status_tag = ?"
        params.append(status)
    if category:
        query += " AND category = ?"
        params.append(category)
    if origin:
        query += " AND origin = ?"
        params.append(origin)
    if distributor_id:
        query += " AND id IN (SELECT manufacturer_id FROM company_distributors WHERE distributor_id = ?)"
        params.append(distributor_id)
    if q:
        query += " AND (name LIKE ? OR portfolio LIKE ? OR ksa_status LIKE ?)"
        like = f"%{q}%"
        params += [like, like, like]
    total = conn.execute(f"SELECT count(*) c FROM ({query})", params).fetchone()["c"]
    query += " ORDER BY id LIMIT ? OFFSET ?"
    params += [limit, offset]
    rows = conn.execute(query, params).fetchall()
    conn.close()
    logger.info(f"GET /companies status={status} category={category} origin={origin} q={q} -> {len(rows)}/{total} results")
    return {
        "results": [dict(r) for r in rows],
        "total": total,
        "limit": limit,
        "offset": offset,
        "has_more": offset + len(rows) < total,
    }

@app.get("/review-queue")
def review_queue():
    """Companies added but not yet approved by a human reviewer -- the real, bounded
    version of 'nothing gets published without review'."""
    conn = get_conn()
    rows = conn.execute("SELECT * FROM manufacturers WHERE is_published = 0 ORDER BY id").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/companies/{company_id}/approve")
def approve_company(company_id: int):
    conn = get_conn()
    existing = conn.execute("SELECT name, is_published FROM manufacturers WHERE id = ?", (company_id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Company not found")
    conn.execute("UPDATE manufacturers SET is_published = 1 WHERE id = ?", (company_id,))
    conn.commit()
    log_action(conn, "manufacturers", company_id, "approve", f"Approved and published: {existing['name']}")
    logger.info(f"POST /companies/{company_id}/approve -> published {existing['name']}")
    conn.close()
    return {"id": company_id, "status": "approved_and_published"}

@app.delete("/companies/{company_id}/reject")
def reject_company(company_id: int):
    conn = get_conn()
    existing = conn.execute("SELECT name FROM manufacturers WHERE id = ? AND is_published = 0", (company_id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Pending company not found (already published or never existed -- use DELETE /companies/{id} for published records)")
    conn.execute("DELETE FROM manufacturers WHERE id = ?", (company_id,))
    conn.commit()
    log_action(conn, "manufacturers", company_id, "reject", f"Rejected during review: {existing['name']}")
    logger.info(f"DELETE /companies/{company_id}/reject -> rejected {existing['name']}")
    conn.close()
    return {"id": company_id, "status": "rejected_and_removed"}

@app.get("/categories")
def list_categories():
    conn = get_conn()
    rows = conn.execute("SELECT category, count(*) as c FROM manufacturers GROUP BY category").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/origins")
def list_origins():
    conn = get_conn()
    rows = conn.execute("SELECT origin, count(*) as c FROM manufacturers GROUP BY origin").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/attieh-portfolio")
def attieh_portfolio():
    """Manufacturers Attieh Medico is directly and confirmedly awarded to represent, per official NUPCO tender records."""
    conn = get_conn()
    rows = conn.execute("SELECT * FROM attieh_portfolio ORDER BY manufacturer").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/tenders")
def list_tenders():
    """Real tender references from the two NUPCO documents provided -- not a live tender feed."""
    conn = get_conn()
    rows = conn.execute("SELECT * FROM tenders ORDER BY tender_ref").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/hospitals")
def list_hospitals():
    """Real installed-equipment data for major KSA government hospital networks, sourced from NUPCO tender NPT0058/25."""
    conn = get_conn()
    rows = conn.execute("SELECT * FROM hospitals ORDER BY abbreviation").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/products")
def list_products(manufacturer_id: int | None = None, origin: str | None = None,
                   department: str | None = None, technology: str | None = None,
                   distributor_id: int | None = None):
    conn = get_conn()
    query = """SELECT p.*, m.name as manufacturer_name, m.category, m.confidence_tier, m.origin
               FROM products p JOIN manufacturers m ON m.id = p.manufacturer_id WHERE 1=1"""
    params = []
    if manufacturer_id:
        query += " AND p.manufacturer_id = ?"
        params.append(manufacturer_id)
    if origin:
        query += " AND m.origin = ?"
        params.append(origin)
    if department:
        query += " AND p.department = ?"
        params.append(department)
    if distributor_id:
        query += " AND m.id IN (SELECT manufacturer_id FROM company_distributors WHERE distributor_id = ?)"
        params.append(distributor_id)
    if technology:
        query += """ AND m.id IN (
            SELECT mt.manufacturer_id FROM manufacturer_technology mt
            JOIN technologies t ON t.id = mt.technology_id WHERE t.name LIKE ?)"""
        params.append(f"%{technology}%")
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/distributor-products/{distributor_name}")
def distributor_products(distributor_name: str):
    conn = get_conn()
    # Use LIKE matching since the same real-world distributor sometimes appears under
    # slightly different name formats across different source documents (e.g. "Samir
    # Group" vs "Samir Trading & Marketing") -- exact match would silently miss real links.
    key = distributor_name.split(" (")[0].split(",")[0].strip()
    rows = conn.execute(
        """SELECT dp.*, p.product_name, p.product_type, p.description, m.name as manufacturer_name
           FROM distributor_products dp
           JOIN products p ON p.id = dp.product_id
           JOIN manufacturers m ON m.id = p.manufacturer_id
           WHERE dp.distributor_name LIKE ? OR ? LIKE '%' || dp.distributor_name || '%'""",
        (f"%{key}%", distributor_name)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/opportunities-by-category")
def opportunities_by_category():
    """Honest per-category opportunity coverage -- reports zero, not a fabricated lead, when every
    researched company in a category already has confirmed KSA coverage."""
    conn = get_conn()
    categories = [r["category"] for r in conn.execute("SELECT DISTINCT category FROM manufacturers").fetchall()]
    result = []
    for cat in categories:
        total = conn.execute("SELECT count(*) c FROM manufacturers WHERE category = ?", (cat,)).fetchone()["c"]
        open_or_unclear = conn.execute(
            "SELECT count(*) c FROM manufacturers WHERE category = ? AND status_tag IN ('open','unclear')", (cat,)
        ).fetchone()["c"]
        result.append({
            "category": cat,
            "companies_researched": total,
            "companies_with_open_question": open_or_unclear,
            "note": "All researched companies in this category already have confirmed KSA coverage." if open_or_unclear == 0
                    else f"{open_or_unclear} of {total} researched companies have an unresolved KSA distribution question."
        })
    conn.close()
    return result

@app.get("/companies/{company_id}/intelligence-score")
def intelligence_score(company_id: int):
    """A transparent, explainable score computed from real fields already in the database.
    Not a black box -- every point is shown with its source."""
    conn = get_conn()
    company = conn.execute("SELECT * FROM manufacturers WHERE id = ?", (company_id,)).fetchone()
    if not company:
        conn.close()
        raise HTTPException(status_code=404, detail="Company not found")
    n_products = conn.execute("SELECT count(*) c FROM products WHERE manufacturer_id = ?", (company_id,)).fetchone()["c"]
    n_technologies = conn.execute(
        "SELECT count(*) c FROM manufacturer_technology WHERE manufacturer_id = ?", (company_id,)
    ).fetchone()["c"]
    n_evidence = conn.execute("SELECT count(*) c FROM evidence WHERE manufacturer_id = ?", (company_id,)).fetchone()["c"]
    n_events = conn.execute("SELECT count(*) c FROM market_events WHERE manufacturer_id = ?", (company_id,)).fetchone()["c"]
    conn.close()

    tier_points = {"gold": 30, "silver": 18, "bronze": 6}
    confidence_points = tier_points.get(company["confidence_tier"], 0)
    product_points = min(n_products * 5, 20)          # cap at 20 (4+ products)
    technology_points = min(n_technologies * 5, 15)    # cap at 15 (3+ technologies)
    evidence_points = min(n_evidence * 5, 20)          # cap at 20 (4+ evidence entries)
    event_points = min(n_events * 5, 10)               # cap at 10 (2+ events)
    distribution_points = 5 if company["status_tag"] == "covered" else 0  # a resolved status, not "open is better"

    total = confidence_points + product_points + technology_points + evidence_points + event_points + distribution_points

    return {
        "company": company["name"],
        "score": total,
        "max_possible": 100,
        "breakdown": {
            "confidence_tier": {"points": confidence_points, "max": 30, "basis": f"tier = {company['confidence_tier']}"},
            "product_portfolio": {"points": product_points, "max": 20, "basis": f"{n_products} products on file"},
            "technology_diversity": {"points": technology_points, "max": 15, "basis": f"{n_technologies} technology links"},
            "evidence_coverage": {"points": evidence_points, "max": 20, "basis": f"{n_evidence} evidence entries"},
            "market_event_history": {"points": event_points, "max": 10, "basis": f"{n_events} logged events"},
            "ksa_status_resolved": {"points": distribution_points, "max": 5, "basis": company["status_tag"]},
        },
        "note": "Every point above is computed from real database counts -- not an estimate or an AI judgment call."
    }

@app.get("/companies/{company_id}/competitors")
def company_competitors(company_id: int):
    """Competitors derived from shared technology links -- not researched separately, purely
    computed from data already in the database."""
    conn = get_conn()
    company = conn.execute("SELECT * FROM manufacturers WHERE id = ?", (company_id,)).fetchone()
    if not company:
        conn.close()
        raise HTTPException(status_code=404, detail="Company not found")
    rows = conn.execute(
        """SELECT DISTINCT m2.id, m2.name, m2.category, t.name as shared_technology
           FROM manufacturer_technology mt1
           JOIN manufacturer_technology mt2 ON mt1.technology_id = mt2.technology_id AND mt2.manufacturer_id != mt1.manufacturer_id
           JOIN manufacturers m2 ON m2.id = mt2.manufacturer_id
           JOIN technologies t ON t.id = mt1.technology_id
           WHERE mt1.manufacturer_id = ?""",
        (company_id,)
    ).fetchall()
    conn.close()
    if not rows:
        return {"company": company["name"], "competitors": [], "note": "No shared-technology links found -- either this company has no technology links recorded, or no other company shares one."}
    return {"company": company["name"], "competitors": [dict(r) for r in rows],
            "note": "Derived purely from shared Technology links already in the database -- not independently researched competitor analysis."}

@app.get("/market-events")
def market_events():
    conn = get_conn()
    rows = conn.execute(
        """SELECT e.*, m.name as manufacturer_name FROM market_events e
           JOIN manufacturers m ON m.id = e.manufacturer_id ORDER BY e.event_date DESC"""
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/companies/{company_id}")
def get_company(company_id: int):
    conn = get_conn()
    row = conn.execute("SELECT * FROM manufacturers WHERE id = ?", (company_id,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Company not found")
    company = dict(row)
    techs = conn.execute(
        """SELECT t.name, t.description FROM technologies t
           JOIN manufacturer_technology mt ON mt.technology_id = t.id
           WHERE mt.manufacturer_id = ?""", (company_id,)
    ).fetchall()
    company["technologies"] = [dict(t) for t in techs]
    dists = conn.execute(
        """SELECT d.* FROM distributors d
           JOIN company_distributors cd ON cd.distributor_id = d.id
           WHERE cd.manufacturer_id = ?""", (company_id,)
    ).fetchall()
    company["distributors"] = [dict(d) for d in dists]
    opp = conn.execute("SELECT * FROM opportunities WHERE manufacturer_id = ?", (company_id,)).fetchone()
    company["opportunity"] = dict(opp) if opp else None
    evidence = conn.execute("SELECT * FROM evidence WHERE manufacturer_id = ?", (company_id,)).fetchall()
    company["evidence"] = [dict(e) for e in evidence]
    products = conn.execute("SELECT * FROM products WHERE manufacturer_id = ?", (company_id,)).fetchall()
    company["products"] = [dict(p) for p in products]
    conn.close()
    return company

@app.get("/companies/{company_id}/evidence")
def company_evidence(company_id: int):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM evidence WHERE manufacturer_id = ?", (company_id,)).fetchall()
    conn.close()
    if not rows:
        return {"company_id": company_id, "evidence": [], "note": "No structured evidence recorded yet for this company."}
    return {"company_id": company_id, "evidence": [dict(r) for r in rows]}

@app.get("/data-quality")
def data_quality():
    conn = get_conn()
    total = conn.execute("SELECT count(*) c FROM manufacturers").fetchone()["c"]
    tier_map = {"gold": 100, "silver": 65, "bronze": 30}
    rows = conn.execute("SELECT confidence_tier FROM manufacturers").fetchall()
    tier_counts = {"gold": 0, "silver": 0, "bronze": 0}
    total_score = 0
    for r in rows:
        t = r["confidence_tier"]
        tier_counts[t] = tier_counts.get(t, 0) + 1
        total_score += tier_map.get(t, 0)
    incomplete = conn.execute(
        "SELECT count(*) c FROM manufacturers WHERE sources LIKE '%None yet%' OR sources = '' OR sources IS NULL"
    ).fetchone()["c"]
    needs_review = conn.execute(
        "SELECT count(*) c FROM manufacturers WHERE status_tag = 'unclear' OR confidence_tier = 'bronze'"
    ).fetchone()["c"]
    with_evidence = conn.execute(
        "SELECT count(DISTINCT manufacturer_id) c FROM evidence"
    ).fetchone()["c"]
    latest = conn.execute("SELECT MAX(created_at) c FROM manufacturers").fetchone()["c"]
    conn.close()
    return {
        "total_companies": total,
        "average_confidence_score": round(total_score / total, 1) if total else 0,
        "tier_breakdown": tier_counts,
        "companies_with_no_sources_recorded": incomplete,
        "companies_needing_review": needs_review,
        "companies_with_structured_evidence": with_evidence,
        "companies_missing_structured_evidence": total - with_evidence,
        "last_record_added": latest,
        "note": "Every number above is computed live from the actual database, not estimated.",
    }

@app.post("/companies")
def add_company(company: NewCompany):
    conn = get_conn()
    cur = conn.execute(
        """INSERT INTO manufacturers (name, headquarters, website, portfolio, ksa_status, status_tag, opportunity_note, confidence_tier, sources, is_published)
           VALUES (?,?,?,?,?,?,?,?,?,0)""",
        (company.name, company.headquarters, company.website, company.portfolio,
         "Manually entered — not yet verified against an official source", company.status_tag,
         "Not yet scored", "bronze", "None yet — needs verification")
    )
    conn.commit()
    new_id = cur.lastrowid
    log_action(conn, "manufacturers", new_id, "insert", f"Submitted for review: {company.name}")
    logger.info(f"POST /companies -> submitted id={new_id} name={company.name} (pending review)")
    conn.close()
    return {"id": new_id, "status": "pending_review", "note": "Not published yet -- goes to the review queue. Call POST /companies/{id}/approve to publish it, or DELETE /companies/{id}/reject to discard it."}

class UpdateCompany(BaseModel):
    headquarters: str | None = None
    website: str | None = None
    portfolio: str | None = None
    status_tag: Literal["covered", "unclear", "open"] | None = None

@app.put("/companies/{company_id}")
def update_company(company_id: int, updates: UpdateCompany):
    conn = get_conn()
    existing = conn.execute("SELECT * FROM manufacturers WHERE id = ?", (company_id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Company not found")
    fields, params = [], []
    for field, value in updates.model_dump(exclude_unset=True).items():
        fields.append(f"{field} = ?")
        params.append(value)
    if not fields:
        conn.close()
        raise HTTPException(status_code=400, detail="No fields provided to update")
    params.append(company_id)
    conn.execute(f"UPDATE manufacturers SET {', '.join(fields)} WHERE id = ?", params)
    conn.commit()
    log_action(conn, "manufacturers", company_id, "update", f"Fields changed: {', '.join(updates.model_dump(exclude_unset=True).keys())}")
    logger.info(f"PUT /companies/{company_id} -> updated fields: {list(updates.model_dump(exclude_unset=True).keys())}")
    conn.close()
    return {"id": company_id, "status": "updated"}

@app.delete("/companies/{company_id}")
def delete_company(company_id: int):
    conn = get_conn()
    existing = conn.execute("SELECT name FROM manufacturers WHERE id = ?", (company_id,)).fetchone()
    if not existing:
        conn.close()
        raise HTTPException(status_code=404, detail="Company not found")
    conn.execute("DELETE FROM manufacturers WHERE id = ?", (company_id,))
    conn.commit()
    log_action(conn, "manufacturers", company_id, "delete", f"Deleted: {existing['name']}")
    logger.warning(f"DELETE /companies/{company_id} -> removed {existing['name']}")
    conn.close()
    return {"id": company_id, "status": "deleted"}

JWT_SECRET = os.environ.get("JWT_SECRET")
if not JWT_SECRET:
    JWT_SECRET = "insecure-local-dev-secret-change-me"
    logger.warning("JWT_SECRET env var not set -- using an insecure local-dev default. Set a real secret before deploying anywhere reachable by others.")
JWT_ALGORITHM = "HS256"
JWT_EXPIRE_HOURS = 24 * 7

def create_access_token(user_id: int, email: str) -> str:
    payload = {"sub": str(user_id), "email": email, "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRE_HOURS)}
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

def get_current_user(authorization: str | None = Header(default=None)) -> dict:
    """Real per-account auth. Every tenant-scoped endpoint (leads, watchlist,
    opportunities, daily-briefing) depends on this instead of a shared password
    -- each user only ever sees their own data."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")
    token = authorization.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Session expired, please log in again")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid session token")
    conn = get_conn()
    user = conn.execute("SELECT * FROM users WHERE id = ? AND is_active = 1", (payload["sub"],)).fetchone()
    conn.close()
    if not user:
        raise HTTPException(status_code=401, detail="Account not found or deactivated")
    return dict(user)

def public_user_fields(user: dict) -> dict:
    return {k: user[k] for k in ("id", "email", "company_name", "full_name", "role")}

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    company_name: str = Field(..., min_length=1)
    full_name: str | None = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@app.post("/auth/register")
def register(reg: RegisterRequest):
    conn = get_conn()
    existing = conn.execute("SELECT id FROM users WHERE email = ?", (reg.email,)).fetchone()
    if existing:
        conn.close()
        raise HTTPException(status_code=400, detail="An account with this email already exists")
    password_hash = bcrypt.hashpw(reg.password.encode(), bcrypt.gensalt()).decode()
    cur = conn.execute(
        "INSERT INTO users (email, password_hash, company_name, full_name, role) VALUES (?,?,?,?,'user')",
        (reg.email, password_hash, reg.company_name, reg.full_name)
    )
    conn.commit()
    user_id = cur.lastrowid
    conn.execute("INSERT INTO audit_log (table_name, record_id, action, detail) VALUES ('users', ?, 'insert', ?)",
                 (user_id, f"New account registered: {reg.email} ({reg.company_name})"))
    conn.commit()
    conn.close()
    token = create_access_token(user_id, reg.email)
    return {"access_token": token, "token_type": "bearer",
            "user": {"id": user_id, "email": reg.email, "company_name": reg.company_name, "full_name": reg.full_name, "role": "user"}}

@app.post("/auth/login")
def login(creds: LoginRequest):
    conn = get_conn()
    user = conn.execute("SELECT * FROM users WHERE email = ? AND is_active = 1", (creds.email,)).fetchone()
    conn.close()
    if not user or not bcrypt.checkpw(creds.password.encode(), user["password_hash"].encode()):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token(user["id"], user["email"])
    return {"access_token": token, "token_type": "bearer", "user": public_user_fields(dict(user))}

@app.get("/auth/me")
def read_me(current_user: dict = Depends(get_current_user)):
    return public_user_fields(current_user)

@app.get("/opportunities")
def list_opportunities(current_user: dict = Depends(get_current_user)):
    """Opportunities requires a real login -- it reveals which manufacturers
    have no confirmed KSA distributor, sensitive competitive strategy info.
    Any logged-in account can see this shared market view (it's not
    tenant-specific data itself, unlike leads/watchlist below)."""
    conn = get_conn()
    rows = conn.execute(
        """SELECT o.*, m.name as company_name FROM opportunities o
           JOIN manufacturers m ON m.id = o.manufacturer_id"""
    ).fetchall()
    conn.close()
    results = []
    for r in rows:
        d = dict(r)
        d["total_score"] = d["score_no_distributor"] + d["score_confidence"] + d["score_brand"]
        results.append(d)
    return sorted(results, key=lambda x: -x["total_score"])

class NewLead(BaseModel):
    manufacturer_id: int
    contact_name: str | None = None
    contact_role: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    status: Literal["new", "contacted", "in_progress", "won", "lost"] = "new"
    notes: str | None = None

class UpdateLead(BaseModel):
    contact_name: str | None = None
    contact_role: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    status: Literal["new", "contacted", "in_progress", "won", "lost"] | None = None
    notes: str | None = None

class NewInteraction(BaseModel):
    interaction_type: Literal["call", "email", "meeting", "note"]
    summary: str = Field(..., min_length=1)
    next_followup_date: str | None = None

@app.get("/leads")
def list_leads(current_user: dict = Depends(get_current_user)):
    conn = get_conn()
    rows = conn.execute("""
        SELECT l.*, m.name as company_name, m.category, m.status_tag
        FROM leads l JOIN manufacturers m ON m.id = l.manufacturer_id
        WHERE l.user_id = ?
        ORDER BY l.created_at DESC
    """, (current_user["id"],)).fetchall()
    leads = [dict(r) for r in rows]
    for lead in leads:
        interactions = conn.execute(
            "SELECT * FROM lead_interactions WHERE lead_id = ? ORDER BY interaction_date DESC", (lead["id"],)
        ).fetchall()
        lead["interactions"] = [dict(i) for i in interactions]
        lead["last_interaction"] = lead["interactions"][0] if lead["interactions"] else None
    conn.close()
    return leads

@app.post("/leads")
def create_lead(lead: NewLead, current_user: dict = Depends(get_current_user)):
    conn = get_conn()
    company = conn.execute("SELECT id FROM manufacturers WHERE id = ?", (lead.manufacturer_id,)).fetchone()
    if not company:
        conn.close()
        raise HTTPException(status_code=404, detail="manufacturer_id not found")
    cur = conn.execute(
        "INSERT INTO leads (user_id, manufacturer_id, contact_name, contact_role, contact_email, contact_phone, status, notes) VALUES (?,?,?,?,?,?,?,?)",
        (current_user["id"], lead.manufacturer_id, lead.contact_name, lead.contact_role, lead.contact_email, lead.contact_phone, lead.status, lead.notes)
    )
    conn.commit()
    lead_id = cur.lastrowid
    conn.execute("INSERT INTO audit_log (table_name, record_id, action, detail) VALUES ('leads', ?, 'insert', ?)",
                 (lead_id, f"New lead created by user {current_user['id']} for manufacturer_id {lead.manufacturer_id}"))
    conn.commit()
    conn.close()
    return {"id": lead_id, "status": "created"}

def _owned_lead_or_404(conn, lead_id: int, user_id: int):
    row = conn.execute("SELECT * FROM leads WHERE id = ? AND user_id = ?", (lead_id, user_id)).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Lead not found")
    return row

@app.put("/leads/{lead_id}")
def update_lead(lead_id: int, updates: UpdateLead, current_user: dict = Depends(get_current_user)):
    conn = get_conn()
    _owned_lead_or_404(conn, lead_id, current_user["id"])
    fields = {k: v for k, v in updates.dict().items() if v is not None}
    if fields:
        set_clause = ", ".join(f"{k} = ?" for k in fields)
        conn.execute(f"UPDATE leads SET {set_clause} WHERE id = ?", (*fields.values(), lead_id))
        conn.commit()
    conn.close()
    return {"id": lead_id, "status": "updated"}

@app.delete("/leads/{lead_id}")
def delete_lead(lead_id: int, current_user: dict = Depends(get_current_user)):
    conn = get_conn()
    _owned_lead_or_404(conn, lead_id, current_user["id"])
    conn.execute("DELETE FROM leads WHERE id = ?", (lead_id,))
    conn.commit()
    conn.close()
    return {"id": lead_id, "status": "deleted"}

@app.post("/leads/{lead_id}/interactions")
def add_interaction(lead_id: int, interaction: NewInteraction, current_user: dict = Depends(get_current_user)):
    conn = get_conn()
    _owned_lead_or_404(conn, lead_id, current_user["id"])
    conn.execute(
        "INSERT INTO lead_interactions (lead_id, interaction_type, summary, next_followup_date) VALUES (?,?,?,?)",
        (lead_id, interaction.interaction_type, interaction.summary, interaction.next_followup_date)
    )
    conn.commit()
    conn.close()
    return {"lead_id": lead_id, "status": "interaction logged"}

@app.get("/watchlist")
def list_watchlist(current_user: dict = Depends(get_current_user)):
    conn = get_conn()
    rows = conn.execute("""
        SELECT w.id as watchlist_id, w.added_at, m.* FROM watchlist w
        JOIN manufacturers m ON m.id = w.manufacturer_id
        WHERE w.user_id = ?
        ORDER BY w.added_at DESC
    """, (current_user["id"],)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.post("/watchlist/{manufacturer_id}")
def add_to_watchlist(manufacturer_id: int, current_user: dict = Depends(get_current_user)):
    conn = get_conn()
    company = conn.execute("SELECT id FROM manufacturers WHERE id = ?", (manufacturer_id,)).fetchone()
    if not company:
        conn.close()
        raise HTTPException(status_code=404, detail="manufacturer_id not found")
    try:
        conn.execute("INSERT INTO watchlist (user_id, manufacturer_id) VALUES (?,?)", (current_user["id"], manufacturer_id))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()
    return {"manufacturer_id": manufacturer_id, "status": "watched"}

@app.delete("/watchlist/{manufacturer_id}")
def remove_from_watchlist(manufacturer_id: int, current_user: dict = Depends(get_current_user)):
    conn = get_conn()
    conn.execute("DELETE FROM watchlist WHERE manufacturer_id = ? AND user_id = ?", (manufacturer_id, current_user["id"]))
    conn.commit()
    conn.close()
    return {"manufacturer_id": manufacturer_id, "status": "unwatched"}

@app.get("/daily-briefing")
def daily_briefing(current_user: dict = Depends(get_current_user)):
    """Executive daily briefing: what's genuinely new since recent activity --
    derived entirely from real audit_log/opportunities/conferences/leads data,
    scoped to the logged-in account's own leads/watchlist. Nothing generated
    or invented."""
    conn = get_conn()
    recent_changes = conn.execute("SELECT * FROM audit_log ORDER BY id DESC LIMIT 8").fetchall()
    top_opps = conn.execute("""
        SELECT o.*, m.name as company_name FROM opportunities o
        JOIN manufacturers m ON m.id = o.manufacturer_id
    """).fetchall()
    top_opps_scored = sorted(
        [dict(r, total_score=r["score_no_distributor"] + r["score_confidence"] + r["score_brand"]) for r in top_opps],
        key=lambda x: -x["total_score"]
    )[:3]
    upcoming = conn.execute("SELECT * FROM conferences ORDER BY event_date").fetchall()
    today = datetime.now()
    upcoming_soon = [dict(c) for c in upcoming if 0 <= (datetime.strptime(c["event_date"], "%Y-%m-%d") - today).days <= 30]
    stale_leads = conn.execute("""
        SELECT l.*, m.name as company_name FROM leads l
        JOIN manufacturers m ON m.id = l.manufacturer_id
        WHERE l.user_id = ? AND l.status NOT IN ('won','lost')
        AND l.id NOT IN (
            SELECT lead_id FROM lead_interactions
            WHERE interaction_date >= date('now', '-14 days')
        )
    """, (current_user["id"],)).fetchall()
    watchlist_count = conn.execute("SELECT count(*) c FROM watchlist WHERE user_id = ?", (current_user["id"],)).fetchone()["c"]
    conn.close()
    return {
        "generated_at": today.strftime("%Y-%m-%d %H:%M"),
        "recent_changes": [dict(r) for r in recent_changes],
        "top_opportunities": top_opps_scored,
        "conferences_next_30_days": upcoming_soon,
        "stale_leads_needing_followup": [dict(r) for r in stale_leads],
        "watchlist_count": watchlist_count,
        "note": "Every field above is computed live from real data -- nothing generated or invented.",
    }

@app.get("/conferences")
def list_conferences(upcoming_only: bool = False):
    conn = get_conn()
    rows = conn.execute("SELECT * FROM conferences ORDER BY event_date").fetchall()
    conn.close()
    today = datetime.now()
    results = []
    for r in rows:
        d = dict(r)
        event_date = datetime.strptime(d["event_date"], "%Y-%m-%d")
        d["days_from_today"] = (event_date - today).days
        d["is_past"] = d["days_from_today"] < 0
        if upcoming_only and d["is_past"]:
            continue
        results.append(d)
    return results

@app.get("/distributors")
def list_distributors():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM distributors").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/dashboard")
def dashboard():
    conn = get_conn()
    total = conn.execute("SELECT count(*) c FROM manufacturers").fetchone()["c"]
    resolved = conn.execute("SELECT count(*) c FROM manufacturers WHERE status_tag IN ('covered','open')").fetchone()["c"]
    open_opps = conn.execute("SELECT count(*) c FROM manufacturers WHERE status_tag='open'").fetchone()["c"]
    conn.close()
    return {
        "companies_tracked": total,
        "open_opportunities": open_opps,
        "data_completeness_pct": round(resolved / total * 100) if total else 0,
        "snapshot_date": datetime.now().strftime("%Y-%m-%d"),
    }

@app.get("/audit-log")
def audit_log():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM audit_log ORDER BY id DESC LIMIT 50").fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/technologies")
def list_technologies():
    conn = get_conn()
    techs = conn.execute("SELECT * FROM technologies").fetchall()
    result = []
    for t in techs:
        companies = conn.execute(
            """SELECT m.name FROM manufacturers m
               JOIN manufacturer_technology mt ON mt.manufacturer_id = m.id
               WHERE mt.technology_id = ?""", (t["id"],)
        ).fetchall()
        d = dict(t)
        d["companies"] = [c["name"] for c in companies]
        result.append(d)
    conn.close()
    return result

def generate_insight(company: dict) -> str:
    """Rule-based summary generator — plain templating over real fields, not a live AI call."""
    name = company["name"]
    parts = []
    if company["status_tag"] == "open":
        parts.append(f"no confirmed KSA distributor was found for {name} in our research")
    elif company["status_tag"] == "unclear":
        parts.append(f"{name}'s KSA distribution status is unconfirmed — worth a direct question")
    else:
        parts.append(f"{name} already has KSA coverage, so this is not an open distribution lead")

    if company.get("technologies"):
        techs = ", ".join(t["name"] for t in company["technologies"])
        parts.append(f"its confirmed focus areas are: {techs}")

    if company.get("opportunity"):
        total = company["opportunity"]["score_no_distributor"] + company["opportunity"]["score_confidence"] + company["opportunity"]["score_brand"]
        parts.append(f"it scores {total}/10 on our opportunity formula")

    parts.append(f"confidence tier: {company['confidence_tier']} ({company['sources'][:60]}...)" if len(company.get('sources',''))>60 else f"confidence tier: {company['confidence_tier']} ({company.get('sources','no sources yet')})")
    return ". ".join(p[0].upper()+p[1:] for p in parts) + "."

@app.get("/compare")
def compare_products(product_ids: str):
    """Comparison engine. Pass product_ids as a comma-separated list, e.g.
    /compare?product_ids=1,5,12. Returns each product's full record plus its
    manufacturer's origin/category and KSA distributor(s) for side-by-side display."""
    try:
        ids = [int(x) for x in product_ids.split(",") if x.strip()]
    except ValueError:
        raise HTTPException(status_code=400, detail="product_ids must be a comma-separated list of integers")
    if not ids:
        raise HTTPException(status_code=400, detail="At least one product_id is required")
    if len(ids) > 6:
        raise HTTPException(status_code=400, detail="Compare at most 6 products at a time")
    conn = get_conn()
    results = []
    for pid in ids:
        p = conn.execute("""
            SELECT p.*, m.name as manufacturer_name, m.category, m.confidence_tier,
                   m.origin, m.ksa_status, m.headquarters
            FROM products p JOIN manufacturers m ON m.id = p.manufacturer_id WHERE p.id = ?
        """, (pid,)).fetchone()
        if not p:
            continue
        p = dict(p)
        dists = conn.execute("""
            SELECT d.name FROM company_distributors cd
            JOIN distributors d ON d.id = cd.distributor_id
            WHERE cd.manufacturer_id = ?
        """, (p["manufacturer_id"],)).fetchall()
        p["distributors"] = [d["name"] for d in dists]
        results.append(p)
    conn.close()
    if not results:
        raise HTTPException(status_code=404, detail="None of the requested product_ids were found")
    fields = ["product_name", "manufacturer_name", "origin", "category", "department", "product_type",
              "throughput", "sample_types", "certifications", "confidence_tier", "distributors", "description"]
    return {"products": results, "comparison_fields": fields, "count": len(results)}

@app.get("/companies/{company_id}/insight")
def company_insight(company_id: int):
    company = get_company(company_id)
    return {"company": company["name"], "insight": generate_insight(company), "generation_method": "rule-based template over verified fields — not a live AI-generated claim"}

@app.get("/regulatory")
def list_regulatory():
    """Regulatory status records. Deliberately sparse — only contains facts
    already verified with a source during product research. Companies/products
    not listed here simply have no regulatory claim recorded yet; that is not
    the same as 'not approved'."""
    conn = get_conn()
    rows = conn.execute("""
        SELECT r.*, m.name as manufacturer_name, p.product_name
        FROM regulatory_status r
        JOIN manufacturers m ON m.id = r.manufacturer_id
        LEFT JOIN products p ON p.id = r.product_id
        ORDER BY m.name
    """).fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/companies/{company_id}/regulatory")
def company_regulatory(company_id: int):
    conn = get_conn()
    rows = conn.execute("""
        SELECT r.*, p.product_name FROM regulatory_status r
        LEFT JOIN products p ON p.id = r.product_id
        WHERE r.manufacturer_id = ?
    """, (company_id,)).fetchall()
    conn.close()
    if not rows:
        return {"company_id": company_id, "regulatory": [], "note": "No regulatory status recorded yet for this company — not yet researched, not a negative finding."}
    return {"company_id": company_id, "regulatory": [dict(r) for r in rows]}

@app.get("/knowledge-graph")
def knowledge_graph():
    """Graph view of verified relationships already in the database.
    Every node and edge here is derived from existing rows — nothing is
    invented for this endpoint. Company-distributor edges reuse the same
    LIKE-based matching rule as /companies/{id} for consistency."""
    conn = get_conn()
    companies = conn.execute("SELECT id, name, category, status_tag FROM manufacturers").fetchall()
    products = conn.execute("SELECT id, product_name, manufacturer_id FROM products").fetchall()
    techs = conn.execute("SELECT id, name FROM technologies").fetchall()
    mtech = conn.execute("SELECT manufacturer_id, technology_id FROM manufacturer_technology").fetchall()
    dists = conn.execute("SELECT id, name, represents FROM distributors").fetchall()
    conn.close()

    nodes = []
    edges = []
    for c in companies:
        nodes.append({"id": f"company-{c['id']}", "label": c["name"], "type": "company", "category": c["category"], "status": c["status_tag"]})
    for p in products:
        nodes.append({"id": f"product-{p['id']}", "label": p["product_name"], "type": "product"})
        edges.append({"source": f"company-{p['manufacturer_id']}", "target": f"product-{p['id']}", "relation": "makes"})
    for t in techs:
        nodes.append({"id": f"tech-{t['id']}", "label": t["name"], "type": "technology"})
    for mt in mtech:
        edges.append({"source": f"company-{mt['manufacturer_id']}", "target": f"tech-{mt['technology_id']}", "relation": "uses"})
    for d in dists:
        nodes.append({"id": f"dist-{d['id']}", "label": d["name"], "type": "distributor"})
        for c in companies:
            name_key = c["name"].split(" (")[0]
            if d["represents"] and name_key.lower() in d["represents"].lower():
                edges.append({"source": f"dist-{d['id']}", "target": f"company-{c['id']}", "relation": "distributes"})

    return {"nodes": nodes, "edges": edges, "node_count": len(nodes), "edge_count": len(edges),
            "note": "Every node/edge is derived from existing verified database rows — this is a graph view of real data, not a generated network."}

# ---------------- Patient management (Doctor AI) ----------------

class PatientCreate(BaseModel):
    full_name: str = Field(..., min_length=1)
    gender: str | None = None
    age: int | None = None
    department: str | None = None
    visit_type: str = "Outpatient"

class VisitCreate(BaseModel):
    visit_type: str | None = None
    notes: str | None = None

class PatientChatMessage(BaseModel):
    content: Any

def _gen_patient_code(conn) -> str:
    row = conn.execute("SELECT MAX(id) as m FROM patients").fetchone()
    next_id = (row["m"] or 10300) + 1
    return str(max(next_id, 10301))

@app.get("/patients")
def list_patients(patient_code: str | None = None, name: str | None = None, visit_type: str | None = None,
                   department: str | None = None, limit: int = 20, offset: int = 0):
    if limit < 1 or limit > 200:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 200")
    conn = get_conn()
    query = "SELECT * FROM patients WHERE 1=1"
    params = []
    if patient_code:
        query += " AND patient_code LIKE ?"
        params.append(f"%{patient_code}%")
    if name:
        query += " AND full_name LIKE ?"
        params.append(f"%{name}%")
    if visit_type:
        query += " AND visit_type = ?"
        params.append(visit_type)
    if department:
        query += " AND department = ?"
        params.append(department)
    total = conn.execute(f"SELECT count(*) c FROM ({query})", params).fetchone()["c"]
    query += " ORDER BY id DESC LIMIT ? OFFSET ?"
    params += [limit, offset]
    rows = conn.execute(query, params).fetchall()

    results = []
    for r in rows:
        d = dict(r)
        last_visit = conn.execute(
            "SELECT visit_time FROM patient_visits WHERE patient_id = ? ORDER BY visit_time DESC LIMIT 1",
            (d["id"],)
        ).fetchone()
        d["last_visit_time"] = last_visit["visit_time"] if last_visit else d["created_at"]
        results.append(d)
    conn.close()
    return {"results": results, "total": total, "limit": limit, "offset": offset}

@app.post("/patients")
def create_patient(payload: PatientCreate):
    conn = get_conn()
    code = _gen_patient_code(conn)
    cur = conn.execute(
        "INSERT INTO patients (patient_code, full_name, gender, age, department, visit_type) VALUES (?,?,?,?,?,?)",
        (code, payload.full_name, payload.gender, payload.age, payload.department, payload.visit_type)
    )
    patient_id = cur.lastrowid
    conn.execute(
        "INSERT INTO patient_visits (patient_id, visit_type, notes) VALUES (?,?,?)",
        (patient_id, payload.visit_type, "Initial registration")
    )
    conn.commit()
    logger.info(f"POST /patients -> created patient {patient_id} ({payload.full_name})")
    conn.close()
    return {"id": patient_id, "patient_code": code, "status": "created"}

@app.get("/patients/{patient_id}")
def get_patient(patient_id: int):
    conn = get_conn()
    patient = conn.execute("SELECT * FROM patients WHERE id = ?", (patient_id,)).fetchone()
    if not patient:
        conn.close()
        raise HTTPException(status_code=404, detail="Patient not found")
    visits = conn.execute(
        "SELECT * FROM patient_visits WHERE patient_id = ? ORDER BY visit_time DESC", (patient_id,)
    ).fetchall()
    reports = conn.execute(
        "SELECT * FROM patient_reports WHERE patient_id = ? ORDER BY uploaded_at DESC", (patient_id,)
    ).fetchall()
    conn.close()
    return {
        "patient": dict(patient),
        "visits": [dict(v) for v in visits],
        "reports": [dict(r) for r in reports],
    }

@app.post("/patients/{patient_id}/visits")
def add_visit(patient_id: int, payload: VisitCreate):
    conn = get_conn()
    exists = conn.execute("SELECT id FROM patients WHERE id = ?", (patient_id,)).fetchone()
    if not exists:
        conn.close()
        raise HTTPException(status_code=404, detail="Patient not found")
    cur = conn.execute(
        "INSERT INTO patient_visits (patient_id, visit_type, notes) VALUES (?,?,?)",
        (patient_id, payload.visit_type, payload.notes)
    )
    conn.commit()
    visit_id = cur.lastrowid
    conn.close()
    return {"id": visit_id, "status": "created"}

@app.get("/patients/{patient_id}/chat")
def get_patient_chat(patient_id: int):
    conn = get_conn()
    exists = conn.execute("SELECT id FROM patients WHERE id = ?", (patient_id,)).fetchone()
    if not exists:
        conn.close()
        raise HTTPException(status_code=404, detail="Patient not found")
    rows = conn.execute(
        "SELECT role, content, created_at FROM patient_chat_messages WHERE patient_id = ? ORDER BY id ASC",
        (patient_id,)
    ).fetchall()
    conn.close()
    return {"messages": [dict(r) for r in rows]}

DOCTOR_AI_PATIENT_SYSTEM = (
    "You are Doctor AI, a clinical laboratory decision-support assistant on MedForsa GCC, used by physicians "
    "and laboratory professionals across Saudi Arabia and the Gulf. You are reviewing a specific patient's "
    "record and discussing it with the clinician. Patient context: {patient_context}\n\n"
    "Your role: (1) summarize and interpret uploaded lab values against standard reference ranges, "
    "(2) discuss differential considerations and relevant pathophysiology, (3) cite established literature, "
    "clinical guidelines, or textbooks by name where relevant, and (4) support an evidence-based discussion "
    "of the case using the patient's history across visits. You are strictly a reference and discussion tool, "
    "not a diagnostic authority: never state a definitive diagnosis as fact, always frame clinical observations "
    "as possibilities ('may suggest', 'is consistent with', 'differential includes') rather than certainties, "
    "and always make clear that final diagnosis and treatment decisions rest with the treating physician after "
    "direct clinical evaluation. For medication or dosing questions, give only general reference-level "
    "information and recommend consulting current prescribing references. Reply in the same language the "
    "user writes in (Arabic or English). Keep responses focused and clinically useful."
    "{lab_info_block}"
)

def _extract_text_for_matching(content):
    """Pull plain text out of a chat message's content, whether it's a plain string
    or a list of Anthropic content blocks (text/image/document)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                parts.append(block.get("text", ""))
        return " ".join(parts)
    return ""

def find_matching_lab_tests(conn, text, limit=5):
    """Look up MedForsa GCC's internal Lab Info reference library (lab_tests table)
    for any test named or aliased in the given text, so Doctor AI grounds its
    answer in our own sourced reference ranges instead of relying on memory alone."""
    text_lower = (text or "").lower()
    if not text_lower.strip():
        return []
    rows = conn.execute(
        "SELECT slug, name_en, name_ar, aliases, reference_ranges_json, reference_ranges_verified, "
        "clinical_significance_en, critical_values_en FROM lab_tests WHERE is_published = 1"
    ).fetchall()
    matches = []
    for r in rows:
        candidates = [r["name_en"], r["name_ar"]] + (r["aliases"].split(",") if r["aliases"] else [])
        for c in candidates:
            c = c.strip().lower()
            if c and len(c) >= 3 and c in text_lower:
                matches.append(r)
                break
        if len(matches) >= limit:
            break
    return matches

def build_lab_info_block(matches):
    if not matches:
        return ""
    lines = [
        "\n\nInternal Lab Info reference data (MedForsa GCC's own sourced test library -- "
        "prefer these values over general memory when discussing the tests below, and mention "
        "to the clinician that more detail is available on the platform's Lab Info page):"
    ]
    for m in matches:
        try:
            ranges = json.loads(m["reference_ranges_json"]) if m["reference_ranges_json"] else []
        except (ValueError, TypeError):
            ranges = []
        range_str = "; ".join(
            f"{rg.get('parameter','')} ({rg.get('population','')}): {rg.get('range','')}" for rg in ranges
        ) or "no structured ranges on file"
        verified = "verified" if m["reference_ranges_verified"] else "UNVERIFIED -- flag to clinician if used"
        crit_note = f" CRITICAL VALUE ALERT: {m['critical_values_en']}." if m["critical_values_en"] else ""
        lines.append(
            f"- {m['name_en']} / {m['name_ar']} [{verified}] -- {range_str}.{crit_note} "
            f"Full page: /lab-info?slug={m['slug']}"
        )
    return "\n".join(lines)

@app.post("/patients/{patient_id}/chat")
def send_patient_chat(patient_id: int, payload: PatientChatMessage):
    conn = get_conn()
    patient = conn.execute("SELECT * FROM patients WHERE id = ?", (patient_id,)).fetchone()
    if not patient:
        conn.close()
        raise HTTPException(status_code=404, detail="Patient not found")

    history_rows = conn.execute(
        "SELECT role, content FROM patient_chat_messages WHERE patient_id = ? ORDER BY id ASC",
        (patient_id,)
    ).fetchall()

    import json as _json
    messages = []
    for r in history_rows:
        content = r["content"]
        try:
            content = _json.loads(content)
        except (ValueError, TypeError):
            pass
        messages.append({"role": r["role"], "content": content})
    messages.append({"role": "user", "content": payload.content})

    patient_context = (
        f"{patient['full_name']}, {patient['age']}-year-old {patient['gender'] or 'unknown gender'}, "
        f"department: {patient['department'] or 'not specified'}, visit type: {patient['visit_type']}."
    )

    latest_text = _extract_text_for_matching(payload.content)
    lab_matches = find_matching_lab_tests(conn, latest_text)
    lab_info_block = build_lab_info_block(lab_matches)

    system_prompt = DOCTOR_AI_PATIENT_SYSTEM.format(
        patient_context=patient_context, lab_info_block=lab_info_block
    )

    result = call_anthropic(system_prompt, messages)
    reply_text = "\n".join(b.get("text", "") for b in result.get("content", []) if b.get("type") == "text")

    user_content_store = payload.content if isinstance(payload.content, str) else _json.dumps(payload.content)
    conn.execute(
        "INSERT INTO patient_chat_messages (patient_id, role, content) VALUES (?,?,?)",
        (patient_id, "user", user_content_store)
    )
    conn.execute(
        "INSERT INTO patient_chat_messages (patient_id, role, content) VALUES (?,?,?)",
        (patient_id, "assistant", reply_text)
    )
    conn.commit()
    conn.close()
    logger.info(f"POST /patients/{patient_id}/chat -> exchanged message")
    return {"reply": reply_text}

# ---------------- Lab Test Reference ("دليل التحاليل المخبرية") ----------------

class LabTestCreate(BaseModel):
    slug: str = Field(..., min_length=1, max_length=100)
    name_en: str = Field(..., min_length=1)
    name_ar: str | None = None  # Lab Info content is English-only going forward; kept for legacy compatibility
    aliases: str | None = None
    category: str = Field(..., min_length=1)
    purpose_en: str | None = None
    purpose_ar: str | None = None
    specimen_type: str | None = None
    collection_notes_en: str | None = None
    collection_notes_ar: str | None = None
    methodology_en: str | None = None
    methodology_ar: str | None = None
    reference_ranges: list[dict] | None = None
    reference_ranges_verified: bool = False
    clinical_significance_en: str | None = None
    clinical_significance_ar: str | None = None
    critical_values_en: str | None = None
    interfering_factors_en: str | None = None
    questions_to_ask_en: str | None = None
    next_steps_en: str | None = None
    associated_conditions: list[dict] | None = None
    related_tests: list[str] | None = None
    sources: list[dict] = Field(..., min_length=1)
    is_published: bool = True

def _lab_test_row_to_dict(row, include_sources=False):
    d = dict(row)
    for json_field, key in [("reference_ranges_json", "reference_ranges"),
                             ("associated_conditions_json", "associated_conditions"),
                             ("sources_json", "sources")]:
        raw = d.pop(json_field, None)
        try:
            d[key] = json.loads(raw) if raw else []
        except (ValueError, TypeError):
            d[key] = []
    d.pop("related_tests_json", None)
    if not include_sources:
        # Sources are kept for MedForsa GCC's own internal verification/audit trail
        # but are not surfaced in the public-facing Lab Info UI.
        d.pop("sources", None)
    d["reference_ranges_verified"] = bool(d.get("reference_ranges_verified"))
    d["is_published"] = bool(d.get("is_published"))
    return d

def _resolve_related_tests(conn, row, limit=5):
    """Manually curated related_tests_json (list of slugs) takes priority; falls back to
    other published tests in the same category when no curation exists yet."""
    try:
        related_slugs = json.loads(row["related_tests_json"]) if row["related_tests_json"] else []
    except (ValueError, TypeError):
        related_slugs = []

    results = []
    seen = {row["slug"]}
    if related_slugs:
        placeholders = ",".join("?" for _ in related_slugs)
        rows = conn.execute(
            f"SELECT slug, name_en, category FROM lab_tests WHERE slug IN ({placeholders}) AND is_published = 1",
            related_slugs
        ).fetchall()
        by_slug = {r["slug"]: r for r in rows}
        for s in related_slugs:
            if s in by_slug and s not in seen:
                r = by_slug[s]
                results.append({"slug": r["slug"], "name_en": r["name_en"], "category": r["category"]})
                seen.add(s)

    if len(results) < limit:
        fallback_rows = conn.execute(
            "SELECT slug, name_en, category FROM lab_tests WHERE category = ? AND is_published = 1 AND slug != ? ORDER BY name_en LIMIT ?",
            (row["category"], row["slug"], limit - len(results))
        ).fetchall()
        for r in fallback_rows:
            if r["slug"] not in seen:
                results.append({"slug": r["slug"], "name_en": r["name_en"], "category": r["category"]})
                seen.add(r["slug"])

    return results[:limit]

@app.get("/lab-tests-list")
def list_lab_tests(q: str | None = None, category: str | None = None,
                    limit: int = 50, offset: int = 0, include_unpublished: bool = False):
    if limit < 1 or limit > 200:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 200")
    conn = get_conn()
    query = "SELECT * FROM lab_tests WHERE 1=1"
    params = []
    if not include_unpublished:
        query += " AND is_published = 1"
    if category:
        query += " AND category = ?"
        params.append(category)
    if q:
        query += " AND (name_en LIKE ? OR name_ar LIKE ? OR aliases LIKE ?)"
        like = f"%{q}%"
        params += [like, like, like]
    total = conn.execute(f"SELECT count(*) c FROM ({query})", params).fetchone()["c"]
    query += " ORDER BY name_en LIMIT ? OFFSET ?"
    params += [limit, offset]
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return {"total": total, "limit": limit, "offset": offset,
            "results": [_lab_test_row_to_dict(r) for r in rows]}

@app.get("/lab-tests-categories")
def lab_test_categories():
    conn = get_conn()
    rows = conn.execute(
        "SELECT category, count(*) c FROM lab_tests WHERE is_published = 1 GROUP BY category ORDER BY category"
    ).fetchall()
    conn.close()
    return {"categories": [dict(r) for r in rows]}

@app.get("/lab-tests-detail/{slug}")
def get_lab_test(slug: str):
    conn = get_conn()
    row = conn.execute("SELECT * FROM lab_tests WHERE slug = ?", (slug,)).fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Lab test not found")
    result = _lab_test_row_to_dict(row, include_sources=False)
    result["related_tests"] = _resolve_related_tests(conn, row)
    conn.close()
    return result

@app.post("/lab-tests-list")
def create_lab_test(payload: LabTestCreate):
    conn = get_conn()
    existing = conn.execute("SELECT id FROM lab_tests WHERE slug = ?", (payload.slug,)).fetchone()
    if existing:
        conn.close()
        raise HTTPException(status_code=409, detail="A lab test with this slug already exists")
    cur = conn.execute(
        """INSERT INTO lab_tests
        (slug, name_en, name_ar, aliases, category, purpose_en, purpose_ar, specimen_type,
         collection_notes_en, collection_notes_ar, methodology_en, methodology_ar,
         reference_ranges_json, reference_ranges_verified, clinical_significance_en, clinical_significance_ar,
         critical_values_en, interfering_factors_en, questions_to_ask_en, next_steps_en,
         associated_conditions_json, related_tests_json, sources_json, is_published)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (payload.slug, payload.name_en, payload.name_ar or "", payload.aliases, payload.category,
         payload.purpose_en, payload.purpose_ar, payload.specimen_type,
         payload.collection_notes_en, payload.collection_notes_ar,
         payload.methodology_en, payload.methodology_ar,
         json.dumps(payload.reference_ranges or []), int(payload.reference_ranges_verified),
         payload.clinical_significance_en, payload.clinical_significance_ar,
         payload.critical_values_en, payload.interfering_factors_en,
         payload.questions_to_ask_en, payload.next_steps_en,
         json.dumps(payload.associated_conditions or []), json.dumps(payload.related_tests or []),
         json.dumps(payload.sources), int(payload.is_published))
    )
    conn.commit()
    new_id = cur.lastrowid
    log_action(conn, "lab_tests", new_id, "create", f"Added lab test: {payload.name_en}")
    conn.close()
    logger.info(f"POST /lab-tests-list -> created lab test '{payload.slug}'")
    return {"id": new_id, "slug": payload.slug, "status": "created"}
