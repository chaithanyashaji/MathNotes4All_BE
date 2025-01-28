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
PORT = int(os.getenv("PORT", 8000))  # Railway will provide PORT
ENV = os.getenv("ENV", "production")  # Default to 'production'


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
    """Ping endpoint for simple health check."""
    return {"message": "pong"}


@app.get("/health")
async def health():
    """Health check endpoint for Railway."""
    return {"status": "healthy"}


async def keep_alive():
    """Keep the event loop alive."""
    while True:
        try:
            logging.info("[Keep-Alive] Running...")
        except Exception as e:
            logging.error(f"[Keep-Alive Error] {e}")
        await asyncio.sleep(60)  # Log every 60 seconds


@app.on_event("startup")
async def startup_event():
    """Start keep-alive and self-ping tasks on server startup."""
    logging.info("Starting background tasks...")
    asyncio.create_task(keep_alive())  # Keeps the event loop alive
    asyncio.create_task(self_ping())  # Self-ping task


async def self_ping():
    """Periodically logs a self-ping message every 5 minutes."""
    while True:
        try:
            logging.info("[Self-Ping] pong")  # Log a self-ping message
        except Exception as e:
            logging.error(f"[Self-Ping Error] {e}")
        await asyncio.sleep(300)  # Wait for 5 minutes


# Include the calculator router
app.include_router(calculator_router, prefix="/calculate", tags=["calculate"])


if __name__ == "__main__":
    # Run the FastAPI application with Uvicorn
    uvicorn.run(
        "main:app",  # Reference the app instance
        host="0.0.0.0",  # Listen on all available interfaces
        port=PORT,  # Use the dynamic port provided by Railway
        log_level="info"  # Set the logging level
    )
