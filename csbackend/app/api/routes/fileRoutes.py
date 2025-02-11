from fastapi import APIRouter, UploadFile, File, Depends
from sqlmodel import Session
from app.models import File as FileModel
from app.services.minioService import MinioService
from app.api.deps import get_db

router = APIRouter()

minio_service = MinioService("localhost:9000", "C1huBjBICuZmrf3xoii6", "o6yBY3zU6FeWV1C3FLBlLeQAyDMnesZKex4qGaAZ", "ai-folder")

@router.post("/upload")
async def upload_file(file: UploadFile = File(...), session: Session = Depends(get_db)):
    file_data = await file.read()
    file_url = minio_service.upload_file(file_data, file.filename, file.content_type)
    
    if file_url:
        file_record = FileModel(
            file_name=file.filename,
            file_type=file.content_type,
            file_size=len(file_data),
            file_location=file_url,
            storage_type='MinIO'
        )
        session.add(file_record)
        session.commit()
        session.refresh(file_record)
        return {"file_id": file_record.id, "file_url": file_url}
    else:
        return {"error": "File upload failed"}