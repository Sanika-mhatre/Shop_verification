from fastapi import APIRouter, UploadFile, File
from utils.file_handler import save_uploaded_file
from services.ocr_service import extract_text_from_image
from services.banner_parser import parse_banner_details
from services.verification_service import calculate_banner_score
from services.banner_ai_service import detect_banner


router = APIRouter()

@router.post("/scan/banner")
async def scan_banner(file: UploadFile = File(...)):
    file_path = save_uploaded_file(file, "banners")
    ai_result = detect_banner(file_path)
    ai_detection = detect_banner(file_path)

    ocr_result = extract_text_from_image(file_path)

    banner_details = parse_banner_details(
        ocr_result["text"],
        ocr_result["lines"]
    )

    verification = calculate_banner_score(ocr_result, banner_details)

    return {
        "message": "Banner scanned successfully",
        "ai_detection": ai_result,
        "file_path": file_path,
        "filename": file.filename,
        "ocr_result": ocr_result,
        "banner_details": banner_details,
        "banner_ai_detection": ai_detection,
        "verification": verification
    }