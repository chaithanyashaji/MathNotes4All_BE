from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import os
import uvicorn
from apps.calculator.route import router as calculator_router
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
PORT = int(os.getenv("PORT", 8000))  # Railway provides PORT
ENV = os.getenv("ENV", "production")  # Default to 'production'

# Track background tasks for graceful shutdown
tasks = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for setup/teardown logic."""
    logging.info("Application is starting...")
    yield
    logging.info("Application is shutting down...")

# Initialize FastAPI application
app = FastAPI(lifespan=lifespan)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "").split(",") or [
        "http://localhost:5173",  # Local frontend for development
        "https://mathnotes4allbe-production.up.railway.app",  # Deployed backend on Railway
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint to verify the server is running."""
    return {"message": "Server is running"}

@app.get("/health")
async def health():
    """Consolidated health check endpoint."""
    return {"status": "healthy", "ping": "pong"}

async def keep_alive():
    """Keep the event loop alive."""
    while True:
        try:
            logging.info("[Keep-Alive] Running...")
        except Exception as e:
            logging.exception("[Keep-Alive Error]")
        await asyncio.sleep(60)  # Keeps the event loop alive

async def self_ping():
    """Periodically logs a self-ping message every 5 minutes."""
    while True:
        try:
            logging.info("[Self-Ping] pong")  # Log a self-ping message
        except Exception as e:
            logging.exception("[Self-Ping Error]")
        await asyncio.sleep(300)  # Wait for 5 minutes

@app.on_event("startup")
async def startup_event():
    """Start background tasks on server startup."""
    logging.info("Starting background tasks...")
    keep_alive_task = asyncio.create_task(keep_alive())
    self_ping_task = asyncio.create_task(self_ping())
    tasks.extend([keep_alive_task, self_ping_task])

@app.on_event("shutdown")
async def shutdown_event():
    """Cancel background tasks on server shutdown."""
    logging.info("Shutting down background tasks...")
    for task in tasks:
        task.cancel()

# Include the calculator router
app.include_router(calculator_router, prefix="/calculate", tags=["calculate"])

if __name__ == "__main__":
    # Run the FastAPI application with Uvicorn
    uvicorn.run(
        "main:app",  # Reference the app instance
        host="0.0.0.0",  # Listen on all available interfaces
        port=PORT,  # Use the dynamic port provided by Railway
        log_level="info",  # Set the logging level
    )
