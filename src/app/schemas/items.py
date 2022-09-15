from enum import Enum
import re
from fastapi import HTTPException
from pydantic import BaseModel, root_validator
import datetime

regex = r'^(-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$'
match_iso8601 = re.compile(regex).match


def valdate(s):
    try:
        if match_iso8601(s) is not None:
            return True
    except:
        pass
    return False


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
    def vall(cls, v):
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
    def checker(cls, v):
        if v.get('type').value == "FOLDER" and (v.get('url') is not None or v.get('size') is not None):
            raise HTTPException(400, detail="Validation Failed")
        if v.get('type').value == "FILE" and (v.get('size') <= 0 or len(v.get('url')) > 255):
            raise HTTPException(400, detail="Validation Failed")
        return v


class SystemItemImportRequest(BaseModel):
    items: list[SystemItemImport] | None = None
    updateDate: str  # | datetime.datetime

    @root_validator
    def checker(cls, v):
        if not valdate(v.get('updateDate')):
            raise HTTPException(400, detail="Validation Failed")
        return v


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
