from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import String, asc, cast
from sqlmodel import Session, select
import logging

from app.api.deps import get_db
from app.model.conversation import Conversation
from app.model.attachment import Attachment
from app.model.fileAttachment import FileAttachment
from app.model.message import Message
from app.model.messageQuery import MessageQuery
from app.agent.ai_agent import ai_agent
from app.shared.file_storage.minio_file_storage import minioFileStorage

router = APIRouter()
logger = logging.getLogger(__name__)

# Utility function to retrieve conversation
def get_conversation(conversation_id: str, session: Session):
    conversation = session.get(Conversation, conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

# Utility function to retrieve attachments
def get_attachments(conversation_id: str, session: Session):
    conversation = get_conversation(conversation_id, session)

    attachment = session.get(Attachment, conversation.attachment_id)
    if not attachment:
        raise HTTPException(status_code=404, detail="Attachment not found")

    statement = select(FileAttachment).where(FileAttachment.attachment_id == attachment.id)
    file_attachments = session.exec(statement).all()

    if not file_attachments:
        raise HTTPException(status_code=404, detail="No file attachments found")

    return {
        "conversation": conversation,
        "attachment": attachment,
        "file_attachments": file_attachments,
    }

# Utility function to fetch messages
def fetch_messages(conversation_id: str, session: Session):
    statement = (
        select(
            Message.id,
            Message.conversation_id,
            Message.sender,
            MessageQuery.model_name,
            cast(Message.content, String).label("content"),
            cast(MessageQuery.prompt, String).label("prompt"),
            cast(MessageQuery.response, String).label("response"),
        )
        .join(MessageQuery, MessageQuery.message_id == Message.id)
        .where(cast(Message.conversation_id, String) == conversation_id)
        .order_by(asc(MessageQuery.created_at))
    )
    return session.exec(statement).all()

# Utility function to process file attachments and generate messages
async def process_file_attachments(conversation_id: str, model_name: str, session: Session):
    files_data = get_attachments(conversation_id, session)
    file_attachments = files_data.get("file_attachments")
    
    if not file_attachments:
        raise HTTPException(status_code=404, detail="No files found for this conversation")

    for file_attachment in file_attachments:
        try:
            content = minioFileStorage.read(file_attachment.file_name)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to read file: {str(e)}")

        message = create_message(conversation_id, "user", str(content), session)
        response_str = ai_agent.sendMessage(model_name=model_name, prompt=str(content))
        create_message_query(message.id, str(content), response_str, model_name, session)

    # Default message after processing files
    prompt = "Hello, How are you?"
    message = create_message(conversation_id, "user", prompt, session)
    response_str = ai_agent.sendMessage(model_name=model_name, prompt=prompt)
    create_message_query(message.id, prompt, response_str, model_name, session)

# Utility function to create a message
def create_message(conversation_id: str, sender: str, content: str, session: Session):
    message = Message(
        conversation_id=conversation_id,
        sender=sender,
        content=content,
    )
    session.add(message)
    session.commit()
    session.refresh(message)
    return message

# Utility function to create a message query
def  create_message_query(message_id: str, prompt: str, response: str, model_name: str, session: Session):
    message_query = MessageQuery(
        message_id=message_id,
        prompt=prompt,
        response=response,
        model_name=model_name,
        tokens_used=0,
    )
    session.add(message_query)
    session.commit()

@router.get("/conversation/{conversation_id}")
async def get_files_from_conversation(conversation_id: str, session: Session = Depends(get_db)):
    return get_attachments(conversation_id, session)

class ConversationMessageRequest(BaseModel):
    conversation_id: str
    model_name: str

@router.post("/load_session")
async def load_session(request: ConversationMessageRequest, session: Session = Depends(get_db)):
    conversation_id = request.conversation_id
    model_name = request.model_name

    conversation = get_conversation(conversation_id, session)
    messages = fetch_messages(conversation_id, session)

    if not messages:
        await process_file_attachments(conversation_id, model_name, session)

    messages = fetch_messages(conversation_id, session)
    messages_data = [
        {
            "id": message.id,
            "sender": message.sender,
            "content": message.content,
            "prompt": message.prompt,
            "response": message.response,
            "model_name": message.model_name,
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

class SendMessageRequest(BaseModel):
    conversation_id: str
    model_name: str
    send_message: str

@router.post("/send_message")
async def send_message(request: SendMessageRequest, session: Session = Depends(get_db)):
    conversation_id = request.conversation_id
    model_name = request.model_name
    send_message = request.send_message

    conversation = get_conversation(conversation_id, session)
    
    message = create_message(conversation_id, "user", send_message, session)
    response_str = ai_agent.sendMessage(model_name=model_name, prompt=send_message)
    create_message_query(message.id, send_message, response_str, model_name, session)

    messages = fetch_messages(conversation_id, session)
    first_message = messages[-1] if messages else None

    messages_data = (
        {
            "id": first_message.id,
            "sender": first_message.sender,
            "content": first_message.content,
            "prompt": first_message.prompt,
            "response": first_message.response,
            "model_name": first_message.model_name,
        }
        if first_message
        else None
    )

    return {
        "conversation": {
            "id": conversation.id,
            "title": conversation.title,
        },
        "message": messages_data,
    }