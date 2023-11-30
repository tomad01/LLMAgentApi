from typing import Any
from pydantic import BaseModel


class TextInput(BaseModel):
    inputs: str
    parameters: dict[str, Any] | None
