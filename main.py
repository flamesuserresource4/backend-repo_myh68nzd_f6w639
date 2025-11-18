import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import db, create_document, get_documents

app = FastAPI(title="SAT Prep API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic response models
class PlanOut(BaseModel):
    name: str
    price: float
    frequency: str
    features: List[str]
    popular: bool = False

class ReviewOut(BaseModel):
    name: str
    rating: int
    comment: str
    role: Optional[str] = None

class ClassOut(BaseModel):
    title: str
    subtitle: Optional[str] = None
    description: Optional[str] = None
    highlights: List[str] = []

@app.get("/")
def read_root():
    return {"message": "SAT Prep API running"}

@app.get("/api/plans", response_model=List[PlanOut])
def list_plans():
    try:
        docs = get_documents("plan")
        # Map Mongo docs to Pydantic friendly dicts
        return [
            {
                "name": d.get("name", ""),
                "price": float(d.get("price", 0)),
                "frequency": d.get("frequency", "per course"),
                "features": d.get("features", []),
                "popular": bool(d.get("popular", False)),
            }
            for d in docs
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/reviews", response_model=List[ReviewOut])
def list_reviews():
    try:
        docs = get_documents("review")
        return [
            {
                "name": d.get("name", "Anonymous"),
                "rating": int(d.get("rating", 5)),
                "comment": d.get("comment", ""),
                "role": d.get("role"),
            }
            for d in docs
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/class", response_model=ClassOut)
def get_class():
    try:
        docs = get_documents("satclass", limit=1)
        if not docs:
            # Provide sensible defaults if DB empty
            return ClassOut(
                title="Elite SAT Prep",
                subtitle="Score higher with a proven plan",
                description="Focused curriculum, expert tutors, and data-driven practice to raise your score.",
                highlights=[
                    "Small-group and 1:1 options",
                    "Diagnostic + tailored study plan",
                    "Official College Board practice",
                    "Weekly progress reports",
                ],
            )
        d = docs[0]
        return ClassOut(
            title=d.get("title", "SAT Prep"),
            subtitle=d.get("subtitle"),
            description=d.get("description"),
            highlights=d.get("highlights", []),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    import os
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"

    return response

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
