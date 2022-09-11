from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class SystemItem(BaseModel):
    id: str
    url: str | None = None
    date: datetime
    type: Enum
    size: int
    children: list | None = None


class SystemItemImport(BaseModel):
    id: str
    url: str | None = None
    parentId: str
    type: Enum
    size: int


class SystemItemImportRequest(BaseModel):
    items: list[SystemItemImport]
    updateDate: datetime


class SystemItemHistoryUnit(BaseModel):
    id: str
    url: str | None = None
    parentId: str
    type: Enum
    size: int
    date: datetime


class SystemItemHistoryResponse(BaseModel):
    items: list[SystemItemHistoryUnit]


class Error(BaseModel):
    code: int
    message: str
