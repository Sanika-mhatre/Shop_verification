from fastapi import FastAPI
from routes.banner_routes import router as banner_router
from routes.segmentation_routes import router as segmentation_router
from routes.selfie_routes import router as selfie_router
from routes.inside_shop_routes import router as inside_shop_router
from routes.final_verification_routes import router as final_verification_router

app = FastAPI(
    title="AI Shop Verification System",
    version="1.0.0"
)

app.include_router(banner_router)
app.include_router(segmentation_router)
app.include_router(selfie_router)
app.include_router(inside_shop_router)
app.include_router(final_verification_router)

@app.get("/")
def home():
    return {
        "message": "AI Shop Verification Backend Running Successfully"
    }

@app.get("/health")
def health():
    return {
        "status": "Backend Healthy"
    }