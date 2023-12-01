from typing import Any
from pydantic import BaseModel
from enum import Enum

class TaskType(str,Enum):
    CHAT="chat"
    EMAIL="email"
    
class TextInput(BaseModel):
    query: str
    query_type: str
    #parameters: dict[str, Any] | None
