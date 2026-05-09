from ultralytics import YOLO

# Pretrained segmentation model
segmentation_model = YOLO("yolov8n-seg.pt")

def run_yolo_segmentation(image_path: str):
    results = segmentation_model(image_path)

    detections = []

    for result in results:
        if result.boxes is None:
            continue

        for box in result.boxes:
            cls_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = segmentation_model.names[cls_id]

            detections.append({
                "class_name": class_name,
                "confidence": round(confidence * 100, 2)
            })

    unique_classes = list(set([item["class_name"] for item in detections]))

    return {
        "detected_classes": unique_classes,
        "detections": detections,
        "total_detections": len(detections)
    }