from fastapi import APIRouter, UploadFile, File
from utils.file_handler import save_uploaded_file
from services.yolo_segmentation_service import run_yolo_segmentation

router = APIRouter()

@router.post("/scan/segmentation")
async def scan_segmentation(file: UploadFile = File(...)):
    file_path = save_uploaded_file(file, "segmentation")

    result = run_yolo_segmentation(file_path)

    return {
        "message": "YOLOv8 segmentation completed",
        "file_path": file_path,
        "filename": file.filename,
        "segmentation_result": result
    }