def calculate_final_verification(banner_score, selfie_score, inside_shop_score):
    final_score = round(
        (banner_score * 0.4) +
        (selfie_score * 0.3) +
        (inside_shop_score * 0.3),
        2
    )

    warnings = []

    if banner_score < 50:
        warnings.append("Banner verification is weak")

    if selfie_score < 50:
        warnings.append("Selfie verification is weak")

    if inside_shop_score < 50:
        warnings.append("Inside shop verification is weak")

    if final_score >= 75:
        status = "Verified"
    elif final_score >= 50:
        status = "Needs Manual Review"
    else:
        status = "Rejected"

    return {
        "final_score": final_score,
        "verification_status": status,
        "warnings": warnings
    }