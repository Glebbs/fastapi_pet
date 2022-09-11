from fastapi import APIRouter
from src.app.schemas.items import *

router = APIRouter()


@router.post('/imports')
async def import_files(model: SystemItemImportRequest):
    pass


@router.delete('/delete/{id}')
async def import_files(date: datetime):
    pass


@router.get('/nodes/{id}')
async def import_files(id: str):
    pass
