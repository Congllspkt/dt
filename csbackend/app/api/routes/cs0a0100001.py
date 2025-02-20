import logging
import zipfile
import rarfile
from io import BytesIO
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlmodel import Session

from app.shared.file_storage.minio_file_storage import MinioFileStorage
from app.api.deps import get_db
from app.model.attachment import Attachment
from app.model.fileAttachment import FileAttachment
from app.model.conversation import Conversation
from app.shared.file_storage.minio_file_storage import minioFileStorage

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), session: Session = Depends(get_db)):
    file_data = await file.read()
    
    attachment_record = Attachment(
        attachment_name=file.filename,
        description="Uploaded file"
    )
    session.add(attachment_record)
    session.commit()
    session.refresh(attachment_record)

    if zipfile.is_zipfile(BytesIO(file_data)):
        with zipfile.ZipFile(BytesIO(file_data)) as zip_file:
            for zip_info in zip_file.infolist():
                if not zip_info.is_dir():
                    extracted_file_data = zip_file.read(zip_info.filename)
                    file_path = f"{file.filename}/{zip_info.filename}"
                    file_url = minioFileStorage.store(extracted_file_data, file_path, zip_info.filename)
                    
                    if file_url:
                        file_attachment_record = FileAttachment(
                            attachment_id = attachment_record.id,
                            storage_type = MinioFileStorage.StorageType,
                            file_name = zip_info.filename,
                            file_type = zip_info.filename.split('.')[-1],
                            file_size = len(extracted_file_data),
                            file_location = file_url
                        )
                        session.add(file_attachment_record)
                        session.commit()
                        session.refresh(file_attachment_record)
                    else:
                        return {"error": f"Failed to upload {zip_info.filename}"}
                    
    elif rarfile.is_rarfile(BytesIO(file_data)):
        try:
            with rarfile.RarFile(BytesIO(file_data)) as rar_file:
                for rar_info in rar_file.infolist():
                    if not rar_info.isdir():
                        extracted_file_data = rar_file.read(rar_info.filename)
                        folder_name = file.filename.rstrip('.rar')
                        file_path = f"{folder_name}/{rar_info.filename}"
                        file_url = minioFileStorage.store(extracted_file_data, file_path, rar_info.filename)
                    
                        if file_url:
                            file_attachment_record = FileAttachment(
                                attachment_id=attachment_record.id,
                                storage_type = MinioFileStorage.StorageType,
                                file_name=f"{folder_name}/{rar_info.filename}",
                                file_type=rar_info.filename.split('.')[-1],
                                file_size=len(extracted_file_data),
                                file_location=file_url
                            )
                            session.add(file_attachment_record)
                            session.commit()
                            session.refresh(file_attachment_record)
                        else:
                            return {"error": f"Failed to upload {rar_info.filename}"}
        except rarfile.RarCannotExec as e:
            raise HTTPException(status_code=500, detail="Cannot find working tool for extracting .rar files. Please install 'unrar' or 'rar' tool.")
    else:
        file_url = minioFileStorage.store(file_data, file.filename, file.content_type)
        
        if file_url:
            file_attachment_record = FileAttachment(
                attachment_id=attachment_record.id,
                storage_type='MinIO',
                file_name=file.filename,
                file_type=file.content_type,
                file_size=len(file_data),
                file_location=file_url
            )
            session.add(file_attachment_record)
            session.commit()
            session.refresh(file_attachment_record)
        else:
            return {"error": "File upload failed"}

    conversation_record = Conversation(
        attachment_id=attachment_record.id,
        title=file.filename
    )
    session.add(conversation_record)
    session.commit()
    session.refresh(conversation_record)

    return {
        "conversation_id": conversation_record.id
    }