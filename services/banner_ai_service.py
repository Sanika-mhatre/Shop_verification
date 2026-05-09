from ultralytics import YOLO

banner_model = YOLO("models/best.pt")

def detect_banner(image_path):
    results = banner_model(image_path)

    detections = []

    for result in results:
        for box in result.boxes:
            cls_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = banner_model.names[cls_id]

            detections.append({
                "class_name": class_name,
                "confidence": round(confidence * 100, 2)
            })

    return {
        "detected_classes": list(set([d["class_name"] for d in detections])),
        "detections": detections,
        "total_detections": len(detections)
    }