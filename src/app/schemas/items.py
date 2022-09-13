from enum import Enum
from pydantic import BaseModel, ValidationError, validator, root_validator

import datetime


class SystemItemType(str, Enum):
    FILE = "FILE"
    FOLDER = "FOLDER"


def size_folder_rel_check(type: SystemItemType, size: int):
    if not ((type.value == "FILE" and size > 0) or (type.value == "FOLDER" and size == 0)):
        raise ValueError('Size and type does not match')


class SystemItem(BaseModel):
    id: str
    url: str | None = None
    date: datetime.datetime
    parentId: str | None = None
    type: SystemItemType
    size: int | None = None
    children: list = []

    @root_validator()
    def check_passwords_match(cls, v):
        if v.get('type').value == "FOLDER" and v.get('url') is not None:
            raise ValueError('Url should be zero while importing folder')
        if not ((v.get('type').value == "FILE" and 0 < v.get('size') < 256) or (
                v.get('type').value == "FOLDER" and v.get('size') == 0)):
            raise ValueError('Size and type does not match')
        return v

    class Config:
        orm_mode = True


class SystemItemImport(BaseModel):
    id: str
    url: str | None = None
    parentId: str | None = None
    type: SystemItemType
    size: int | None = None


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
