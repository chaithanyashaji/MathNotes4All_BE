from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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
    allow_origins=["https://mathnotes4all.onrender.com/",],  # Add your frontend URL here

    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
async def root():
    return {"message": "Server is running"}

app.include_router(calculator_router, prefix="/calculate", tags=["calculate"])

if __name__ == "__main__":
    # Ensure SERVER_URL is 0.0.0.0 in production for external access
    uvicorn.run("main:app", host="0.0.0.0", port=int(PORT), reload=(ENV == "dev"))
