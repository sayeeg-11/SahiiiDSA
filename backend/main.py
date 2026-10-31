
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.question_routes import router as question_router


app = FastAPI(
    title="SahiiiDSA API",
    description="Backend API for the SahiiiDSA learning platform",
    version="1.0.0",
)

# Allow the React development server to communicate with FastAPI.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(question_router)


@app.get("/")
def root():
    return {
        "message": "Welcome to SahiiiDSA API",
        "status": "running",
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "application": "SahiiiDSA",
    }
