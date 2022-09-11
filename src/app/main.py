from typing import Union
from enum import Enum
from fastapi import FastAPI, Path
from pydantic import BaseModel
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()


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
    items: list[SystemItem]
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


@router.post('/imports')
async def import_files():
    pass
