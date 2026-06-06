from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import books_router, members_router, borrowings_router

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Neighborhood Library Service API",
    description="A complete library management system API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(books_router)
app.include_router(members_router)
app.include_router(borrowings_router)

@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Welcome to Neighborhood Library Service API",
        "docs": "/docs",
        "redoc": "/redoc"
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}
