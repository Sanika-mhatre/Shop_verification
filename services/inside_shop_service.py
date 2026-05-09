from services.yolo_segmentation_service import run_yolo_segmentation
from services.ocr_service import extract_text_from_image

def analyze_inside_shop(image_path: str):
    segmentation = run_yolo_segmentation(image_path)
    ocr_result = extract_text_from_image(image_path)

    detected_classes = segmentation.get("detected_classes", [])
    ocr_text = ocr_result.get("text", "").lower()

    product_keywords = [
        "milk", "oil", "rice", "tea", "coffee", "sugar",
        "detergent", "soap", "shampoo", "biscuit", "snack",
        "medicine", "tablet", "cream", "juice", "water",
        "tide", "persil", "jello", "cake", "powder"
    ]

    detected_product_keywords = [
        word for word in product_keywords
        if word in ocr_text
    ]

    shop_objects = [
        "bottle", "cup", "chair", "tv", "book",
        "refrigerator", "bowl", "box"
    ]

    matched_objects = [
        obj for obj in detected_classes
        if obj in shop_objects
    ]

    score = 0
    warnings = []

    if detected_product_keywords:
        score += 40
    else:
        warnings.append("Product label text not clearly detected")

    if matched_objects:
        score += 30
    else:
        warnings.append("No common shop objects detected")

    if len(detected_classes) >= 2:
        score += 15
    else:
        warnings.append("Few YOLO objects detected")

    if ocr_result.get("confidence", 0) >= 50:
        score += 15
    else:
        warnings.append("OCR confidence is low")

    if score >= 75:
        status = "Valid Inside Shop"
    elif score >= 50:
        status = "Needs Manual Review"
    else:
        status = "Invalid Inside Shop"

    return {
        "detected_classes": detected_classes,
        "matched_shop_objects": matched_objects,
        "detected_product_keywords": list(set(detected_product_keywords)),
        "ocr_text_sample": ocr_result.get("text", "")[:300],
        "ocr_confidence": ocr_result.get("confidence", 0),
        "inside_shop_score": score,
        "status": status,
        "warnings": warnings,
        "segmentation": segmentation
    }