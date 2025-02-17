from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.api.deps import get_db
from app.model.conversation import Conversation
from app.model.attachment import Attachment
from app.model.fileAttachment import FileAttachment

router = APIRouter()

@router.get("/conversation/{conversation_id}")
async def get_files_from_conversation(conversation_id: str, session: Session = Depends(get_db)):
    # Fetch the conversation
    conversation = session.get(Conversation, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Fetch the attachment
    attachment = session.get(Attachment, conversation.attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    # Fetch the file attachments
    statement = select(FileAttachment).where(FileAttachment.attachment_id == attachment.id)
    file_attachments = session.exec(statement).all()

    return {
        "conversation": conversation
        , "attachment": attachment
        , "file_attachments": file_attachments
    }

@router.get("/conversation_message/{conversation_id}")
async def get_files_from_conversation(conversation_id: str, session: Session = Depends(get_db)):

    # add new api get data from conversations table join with messages on conversations.id =   messages.conversation_id
    # return conversations.title, conversations.id, messages.sender, messages.sender, messages.content

    


    return {
        "message": "message"
    }