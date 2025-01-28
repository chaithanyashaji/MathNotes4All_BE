from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import uvicorn
import os
from apps.calculator.route import router as calculator_router

# Load environment variables
PORT = os.getenv("PORT", 8000)  # Default to 8000 if not provided
ENV = os.getenv("ENV", "production")  # Default to 'production'
SERVER_URL = os.getenv("SERVER_URL", "http://localhost")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for the app."""
    yield  # Add any setup/teardown logic here if needed

# Initialize FastAPI application with lifespan
app = FastAPI(lifespan=lifespan)

# Configure CORS to allow requests from the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Local frontend
        "https://mathnotes-nine.vercel.app",  # Deployed frontend
        "https://mathnotes-nine.vercel.app"  # Backend URL
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
        await asyncio.sleep(300)  # Wait for 5 minutes (300 seconds)

@app.on_event("startup")
async def startup_event():
    """Start the self-ping task on server startup."""
    asyncio.create_task(self_ping())

# Include the calculator router
app.include_router(calculator_router, prefix="/calculate", tags=["calculate"])

if __name__ == "__main__":
    # Run the FastAPI application with Uvicorn
    uvicorn.run(
        "main:app",  # Points to the app instance in this file
        host="0.0.0.0",  # Listen on all available interfaces
        port=int(PORT),  # Use the dynamic port from environment variables
        reload=True if ENV == "dev" else False  # Enable reload in development mode
    )
