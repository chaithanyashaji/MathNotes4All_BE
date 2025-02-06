from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import os

# Load environment variables from .env file (for local development)
load_dotenv()

# Get environment variables
ENV = os.getenv("ENV", "dev")  # Default to "dev" if not set
PORT = os.getenv("PORT", 8000)  # Default to 8000 if not set
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")  # Local frontend default

# Async context manager for FastAPI lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

# Initialize FastAPI app
app = FastAPI(lifespan=lifespan)

# CORS Middleware Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        FRONTEND_URL,  # Local frontend or custom URL from environment
        "https://mathnotes-nine.vercel.app"  # Deployed frontend on Vercel
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Root route to verify server status
@app.get("/")
async def root():
    return {"message": "Server is running"}

# Include routes from calculator module
from apps.calculator.route import router as calculator_router
app.include_router(calculator_router, prefix="/calculate", tags=["calculate"])

# Run the application
if __name__ == "__main__":
    # Ensure SERVER_URL is properly set for production
    uvicorn.run(
        "main:app",
        host="0.0.0.0",  # Use 0.0.0.0 for external access
        port=int(PORT),  # Use PORT from environment
        reload=(ENV == "dev")  # Enable reload only in development mode
    )
