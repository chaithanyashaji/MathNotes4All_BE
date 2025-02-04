from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os
from apps.calculator.route import router as calculator_router
from constants import ENV

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

# Allow both local and deployed frontend URLs
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173", 
        os.getenv("FRONTEND_URL", "https://your-deployed-frontend-url.com")  # Fallback to default if not set
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
    # Railway dynamically assigns PORT, use `os.environ`
    port = int(os.getenv("PORT", 8080))  # Defaults to 8080 locally if PORT is not set
    uvicorn.run("main:app", host="0.0.0.0", port=port)

