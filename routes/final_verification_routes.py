from fastapi import APIRouter, UploadFile, File
from utils.file_handler import save_uploaded_file
from services.ocr_service import extract_text_from_image
from services.banner_parser import parse_banner_details
from services.verification_service import calculate_banner_score
from services.selfie_service import analyze_selfie_with_shop
from services.inside_shop_service import analyze_inside_shop
from services.final_verification_service import calculate_final_verification

router = APIRouter()

@router.post("/verify/shop")
async def verify_shop(
    banner: UploadFile = File(...),
    selfie: UploadFile = File(...),
    inside_shop: UploadFile = File(...)
):
    banner_path = save_uploaded_file(banner, "banners")
    selfie_path = save_uploaded_file(selfie, "selfies")
    inside_shop_path = save_uploaded_file(inside_shop, "inside_shop")

    ocr_result = extract_text_from_image(banner_path)

    banner_details = parse_banner_details(
        ocr_result["text"],
        ocr_result["lines"]
    )

    banner_verification = calculate_banner_score(
        ocr_result,
        banner_details
    )

    selfie_result = analyze_selfie_with_shop(selfie_path)
    inside_shop_result = analyze_inside_shop(inside_shop_path)

    final_result = calculate_final_verification(
        banner_verification["banner_score"],
        selfie_result["selfie_score"],
        inside_shop_result["inside_shop_score"]
    )

    return {
        "message": "Final shop verification completed",
        "shop_details": banner_details,
        "banner_verification": banner_verification,
        "selfie_verification": selfie_result,
        "inside_shop_verification": inside_shop_result,
        "final_verification": final_result
    }