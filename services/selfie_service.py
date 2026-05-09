from services.yolo_segmentation_service import run_yolo_segmentation

def analyze_selfie_with_shop(image_path: str):
    segmentation = run_yolo_segmentation(image_path)

    detected_classes = segmentation.get("detected_classes", [])
    detections = segmentation.get("detections", [])

    person_detections = [
        item for item in detections
        if item["class_name"] == "person"
    ]

    warnings = []
    score = 0

    if person_detections:
        score += 50
        person_confidence = max(
            item["confidence"]
            for item in person_detections
        )
    else:
        person_confidence = 0
        warnings.append("Person not detected")

    if person_confidence >= 70:
        score += 20
    elif person_confidence > 0:
        score += 10
        warnings.append("Person confidence is low")

    shop_background_objects = [
        "bottle",
        "cup",
        "chair",
        "tv",
        "book",
        "laptop",
        "refrigerator"
    ]

    background_matches = [
        cls for cls in detected_classes
        if cls in shop_background_objects
    ]

    if background_matches:
        score += 20
    else:
        warnings.append(
            "Shop background not clearly detected"
        )

    if len(detected_classes) >= 2:
        score += 10
    else:
        warnings.append(
            "Image has very few detectable objects"
        )

    if score >= 75:
        status = "Valid Selfie With Shop"
    elif score >= 50:
        status = "Needs Manual Review"
    else:
        status = "Invalid Selfie"

    return {
        "person_detected": len(person_detections) > 0,
        "person_confidence": person_confidence,
        "background_matches": background_matches,
        "selfie_score": score,
        "status": status,
        "warnings": warnings,
        "segmentation": segmentation
    }