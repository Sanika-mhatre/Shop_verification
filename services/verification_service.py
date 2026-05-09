def calculate_banner_score(ocr_result, banner_details):
    score = 0
    warnings = []

    if ocr_result.get("text"):
        score += 20
    else:
        warnings.append("No text detected on banner")

    if ocr_result.get("confidence", 0) >= 50:
        score += 15
    else:
        warnings.append("OCR confidence is low")

    if banner_details.get("shop_name") != "Not Detected":
        score += 20
    else:
        warnings.append("Shop name not detected")

    if banner_details.get("shop_type") != "Unknown":
        score += 15
    else:
        warnings.append("Shop type not detected")

    if banner_details.get("contact_numbers"):
        score += 15
    else:
        warnings.append("Contact number not detected")

    if banner_details.get("services"):
        score += 10
    else:
        warnings.append("Services not detected")

    if banner_details.get("emails") or banner_details.get("websites"):
        score += 5

    if score >= 75:
        status = "Valid Shop Banner"
    elif score >= 50:
        status = "Needs Manual Review"
    else:
        status = "Invalid / Poor Banner"

    return {
        "banner_score": score,
        "banner_status": status,
        "warnings": warnings
    }