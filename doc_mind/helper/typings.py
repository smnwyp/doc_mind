from typing import List

from pydantic import BaseModel


class Context(BaseModel):
    tokens: List[str] = []
    bboxes: List[List[float]] = [[]]


class ChatResponse(BaseModel):
    response: str


class SummarizeResponse(BaseModel):
    response: str
    context: Context


class Message(BaseModel):
    role: str
    content: str


class HistoryMessages(BaseModel):
    msgs: List[Message] = []