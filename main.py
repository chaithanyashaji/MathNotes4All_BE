from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import uvicorn
import os
from apps.calculator.route import router as calculator_router

# Load environment variables
PORT = int(os.getenv("PORT", 8000))  # Railway will provide PORT
ENV = os.getenv("ENV", "production")  # Default to 'production'

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for setup/teardown logic."""
    yield

# Initialize FastAPI application
app = FastAPI(lifespan=lifespan)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local frontend for development
        "https://mathnotes4allbe-production.up.railway.app"  # Deployed backend on Railway
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint to verify the server is running."""
    return {"message": "Server is running"}

@app.get("/ping")
async def ping():
    """Health check endpoint."""
    return {"message": "pong"}

async def self_ping():
    """Periodically logs a self-ping message every 5 minutes."""
    while True:
        try:
            print("[Self-Ping] pong")  # Log a self-ping message
        except Exception as e:
            print(f"[Self-Ping Error] {e}")
        await asyncio.sleep(300)  # Wait for 5 minutes

@app.on_event("startup")
async def startup_event():
    """Start self-ping task on server startup."""
    asyncio.create_task(self_ping())

# Include the calculator router
app.include_router(calculator_router, prefix="/calculate", tags=["calculate"])

if __name__ == "__main__":
    # Run the FastAPI application with Uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Listen on all available interfaces
        port=PORT  # Dynamic port for Railway
    )
