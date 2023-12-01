from typing import Any
from pydantic import BaseModel
from enum import Enum

class TaskType(str,Enum):
    CHAT="chats"
    EMAIL="emails"
    
class TextInput(BaseModel):
    query: str
    query_type: str
    parameters: dict[str, Any] | None
