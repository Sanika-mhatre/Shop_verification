from fastapi import APIRouter, UploadFile, File
from utils.file_handler import save_uploaded_file
from services.inside_shop_service import analyze_inside_shop

router = APIRouter()

@router.post("/scan/inside-shop")
async def scan_inside_shop(file: UploadFile = File(...)):
    file_path = save_uploaded_file(file, "inside_shop")

    result = analyze_inside_shop(file_path)

    return {
        "message": "Inside shop verification completed",
        "file_path": file_path,
        "filename": file.filename,
        "inside_shop_result": result
    }