from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import uvicorn
from apps.calculator.route import router as calculator_router
from constants import SERVER_URL, PORT, ENV

@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

# Allow both local and deployed frontend URLs
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://mathnotes4all.onrender.com","https://mathnotes4all-be.onrender.com"],  # Add your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {"message": "Server is running"}

@app.get('/ping')
async def ping():
    return {"message": "pong"}

async def self_ping():
    """Periodically logs a self-ping message every 5 minutes."""
    while True:
        try:
            # Log a self-ping message or any desired action here
            print("[Self-Ping] pong")
        except Exception as e:
            print(f"[Self-Ping Error] {e}")
        await asyncio.sleep(300)  # Wait for 5 minutes (300 seconds)

@app.on_event("startup")
async def startup_event():
    """Start the self-ping task on server startup."""
    asyncio.create_task(self_ping())

app.include_router(calculator_router, prefix="/calculate", tags=["calculate"])

if __name__ == "__main__":
    # Ensure SERVER_URL is 0.0.0.0 in production for external access
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(PORT),
        reload=True if ENV == "dev" else False  # Reload only in development mode
    )

