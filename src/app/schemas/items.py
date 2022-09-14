from enum import Enum

from fastapi import HTTPException
from pydantic import BaseModel, ValidationError, validator, root_validator
import datetime


class SystemItemType(str, Enum):
    FILE = "FILE"
    FOLDER = "FOLDER"


class SystemItem(BaseModel):
    id: str
    url: str | None = None
    date: datetime.datetime
    parentId: str | None = None
    type: SystemItemType
    size: int | None = None
    children: list = []

    class Config:
        orm_mode = True


class SystemItemImport(BaseModel):
    id: str
    url: str | None = None
    parentId: str | None = None
    type: SystemItemType
    size: int | None = None

    @root_validator
    def check_passwords_match(cls, v):
        if v.get('type').value == "FOLDER" and v.get('url') is not None:
            raise HTTPException(400)
        if not ((v.get('type').value == "FILE" and 0 < v.get('size') and len(v.get('url') < 256)) or (
                v.get('type').value == "FOLDER" and v.get('size') == 0)):
            raise HTTPException(400)
        return v


class SystemItemImportRequest(BaseModel):
    items: list[SystemItemImport]
    updateDate: datetime.datetime


class SystemItemHistoryUnit(BaseModel):
    id: str
    url: str | None = None
    parentId: str
    type: SystemItemType
    size: int
    date: datetime.datetime


class SystemItemHistoryResponse(BaseModel):
    items: list[SystemItemHistoryUnit]

    class Config:
        orm_mode = True


class Error(BaseModel):
    code: int
    message: str

    class Config:
        orm_mode = True
