from paddleocr import PaddleOCR

# English OCR
ocr_english = PaddleOCR(
    use_angle_cls=True,
    lang='en'
)

# Hindi / Marathi OCR
ocr_devanagari = PaddleOCR(
    use_angle_cls=True,
    lang='hi'
)


def _run_ocr(ocr_engine, image_path):
    result = ocr_engine.ocr(image_path, cls=True)

    extracted_text = []
    confidence_scores = []

    if not result or not result[0]:
        return {
            "text": "",
            "lines": [],
            "confidence": 0
        }

    for line in result[0]:
        text = line[1][0]
        confidence = line[1][1]

        extracted_text.append(text)
        confidence_scores.append(confidence)

    avg_confidence = 0

    if confidence_scores:
        avg_confidence = (
            sum(confidence_scores) /
            len(confidence_scores)
        )

    return {
        "text": " ".join(extracted_text),
        "lines": extracted_text,
        "confidence": round(avg_confidence * 100, 2)
    }


def extract_text_from_image(image_path):
    english_result = _run_ocr(
        ocr_english,
        image_path
    )

    devanagari_result = _run_ocr(
        ocr_devanagari,
        image_path
    )

    combined_text = (
        english_result["text"] +
        " " +
        devanagari_result["text"]
    ).strip()

    combined_lines = (
        english_result["lines"] +
        devanagari_result["lines"]
    )

    avg_confidence = round(
        (
            english_result["confidence"] +
            devanagari_result["confidence"]
        ) / 2,
        2
    )

    return {
        "text": combined_text,
        "lines": combined_lines,
        "confidence": avg_confidence,
        "english_ocr": english_result,
        "devanagari_ocr": devanagari_result
    }