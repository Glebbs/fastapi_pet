from fastapi import Request
from enum import Enum
from fastapi.responses import JSONResponse

from fastapi import HTTPException
from pydantic import BaseModel, root_validator
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
    children: list["SystemItem"] | None = None

    @root_validator
    def replace_empty_list(cls, v):
        if v.get('type').value == "FILE":
            v['children'] = None
        v['date'] = str(v['date'].isoformat()) + 'Z'
        return v

    class Config:
        orm_mode = True
        validate_assignment = True


class SystemItemImport(BaseModel):
    id: str
    url: str | None = None
    parentId: str | None = None
    type: SystemItemType
    size: int | None = None

    @root_validator
    def check_passwords_match(cls, v):
        if v.get('type').value == "FOLDER" and (v.get('url') is not None or v.get('size') is not None):
            raise HTTPException(400, detail="Validation Failed")
        if v.get('type').value == "FILE" and (v.get('size') <= 0 or len(v.get('url')) > 255):
            raise HTTPException(400, detail="Validation Failed")
        # if 'Z' and 'T' not in v['date']:
        #     print(v['date'])
        #     raise HTTPException(400, detail="Validation Failed")
        return v


class SystemItemImportRequest(BaseModel):
    items: list[SystemItemImport] | None = None
    updateDate: datetime.datetime


class SystemItemHistoryUnit(BaseModel):
    id: str
    url: str | None = None
    date: datetime.datetime
    parentId: str | None = None
    type: SystemItemType
    size: int | None = None

    class Config:
        orm_mode = True


class SystemItemHistoryResponse(BaseModel):
    items: list[SystemItemHistoryUnit] | None = None

    class Config:
        orm_mode = True


class Error(BaseModel):
    code: int
    message: str

    class Config:
        orm_mode = True
