from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from apps.calculator.route import router as calculator_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI()

# Allow both local and deployed frontend URLs
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        os.getenv("FRONTEND_URL", "https://your-deployed-frontend-url.com")  # Add your deployed frontend URL as fallback
    ],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {"message": "Server is running"}

# Health check route for Railway
@app.get('/health')
async def health():
    return {"status": "healthy"}

app.include_router(calculator_router, prefix="/calculate", tags=["calculate"])

if __name__ == "__main__":
    # Use the PORT environment variable dynamically
    port = int(os.getenv("PORT", 8000))  # Default to 8000 for local testing
    uvicorn.run("main:app", host="0.0.0.0", port=port)
