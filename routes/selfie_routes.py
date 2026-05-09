from fastapi import APIRouter, UploadFile, File
from utils.file_handler import save_uploaded_file
from services.selfie_service import analyze_selfie_with_shop

router = APIRouter()

@router.post("/scan/selfie")
async def scan_selfie(file: UploadFile = File(...)):
    file_path = save_uploaded_file(file, "selfies")

    result = analyze_selfie_with_shop(file_path)

    return {
        "message": "Selfie verification completed",
        "file_path": file_path,
        "filename": file.filename,
        "selfie_result": result
    }