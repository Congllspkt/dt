from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import String, cast
from sqlmodel import Session, select
from app.api.deps import get_db
from app.model.conversation import Conversation
from app.model.attachment import Attachment
from app.model.fileAttachment import FileAttachment
from app.model.message import Message
from app.services.minioService import MinioService
from app.model.messageQuery import MessageQuery

router = APIRouter()
minio_service = MinioService()


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

    if not file_attachments:
        raise HTTPException(status_code=404, detail="No file attachments found")

    return {
        "conversation": conversation,
        "attachment": attachment,
        "file_attachments": file_attachments,
    }


@router.post("/conversation_message/{conversation_id}")
async def load_session(conversation_id: str, session: Session = Depends(get_db)):
    # Fetch the conversation
    conversation = session.get(Conversation, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")

    # Fetch the messages
    messages = fetch_messages(conversation_id, session)

    # If no messages exist, attempt to load from file attachments
    if not messages:
        files_data = await get_files_from_conversation(conversation_id, session)
        file_attachments = files_data.get("file_attachments")

        if not file_attachments:
            raise HTTPException(status_code=404, detail="No files found for this conversation")

        for file_attachment in file_attachments:
            try:
                content = minio_service.read_file(file_attachment.file_name)
                print(content)

            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to read file: {str(e)}")

            message = Message(
                conversation_id=conversation_id,
                sender="111",  # Adjust sender if needed
                content=str(content),  # Ensure content is cast to string
            )
            session.add(message)
            session.commit()
            session.refresh(message)

            # Create a new MessageQuery
            message_query = MessageQuery(
                message_id=message.id,
                prompt=str(""),  # Adjust prompt if needed
                response=str(""),  # Adjust response if needed
                tokens_used=0,  # Adjust tokens if needed
            )
            session.add(message_query)
            session.commit()

        # Fetch messages again after creating them
        messages = fetch_messages(conversation_id, session)

    # Prepare response data
    messages_data = [
        {
            "id": message.id,
            "sender": message.sender,
            "content": message.content_text,  # Use the casted content_text
        }
        for message in messages
    ]

    return {
        "conversation": {
            "id": conversation.id,
            "title": conversation.title,
            "attachment_id": conversation.attachment_id,
        },
        "messages": messages_data,
    }


def fetch_messages(conversation_id: str, session: Session):
    """Fetch messages for a given conversation."""
    statement = select(
        Message.id,
        Message.conversation_id,
        Message.sender,
        cast(Message.content, String).label("content_text"),
    ).where(cast(Message.conversation_id, String) == conversation_id)
    return session.exec(statement).all()