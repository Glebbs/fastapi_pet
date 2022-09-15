from collections import deque
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, update, select, insert
from sqlalchemy.orm import joinedload
from dateutil import parser
from app.schemas import SystemItemImportRequest, SystemItem, SystemItemHistoryResponse
from datetime import timedelta
from app.db.database import get_session
from app.db.models import Items
from app.schemas.items import valdate

router = APIRouter(tags=['Базовые задачи'])


@router.post('/imports', status_code=200)
async def import_files(model: SystemItemImportRequest, session: AsyncSession = Depends(get_session)):
    async with session:
        ids = deque(item.id for item in model.items)
        q = deque(model.items)
        while q:
            item = q.popleft()
            if item.parentId is not None:
                parent = await session.get(Items, item.parentId)
                if parent is None:
                    if item.parentId in ids:
                        q.append(item)
                        continue
                    raise HTTPException(404, detail="Item not found")
                if parent.type.value != 'FOLDER':
                    raise HTTPException(400, detail="Validation Failed")

            old_item = await session.get(Items, item.id)
            if old_item is None:
                await session.execute(insert(Items).values(**item.dict(exclude_none=True),
                                                           date=parser.parse(model.updateDate)))
            else:
                s = old_item.size
                while old_item.parentId:
                    parent = await session.get(Items, old_item.parentId)
                    await session.execute(
                        update(Items).where(Items.id == old_item.parentId).values(
                            date=parser.parse(model.updateDate),
                            size=parent.size - s if parent.size else 0))
                    old_item = parent
                await session.execute(update(Items).where(Items.id == item.id).values(url=item.url,
                                                                                      size=item.size if item.type.value == 'FILE' else s,
                                                                                      type=item.type,
                                                                                      parentId=item.parentId,
                                                                                      date=parser.parse(
                                                                                          model.updateDate)))
            i = await session.get(Items, item.id)
            if i.size:
                s = i.size
                while i.parentId:
                    parent = await session.get(Items, i.parentId)
                    await session.execute(
                        update(Items).where(Items.id == i.parentId).values(date=parser.parse(model.updateDate),
                                                                           size=parent.size + s if parent.size else s))
                    i = parent

        await session.commit()


@router.delete('/delete/{id}', status_code=200)
async def delete_files(date: str, id: str, session: AsyncSession = Depends(get_session)):
    async with session:
        if not valdate(date):
            raise HTTPException(400, detail="Validation Failed")
        item = (await session.execute(select(Items).where(Items.id == id))).scalars().first()
        if item is None:
            raise HTTPException(404, detail="Item not found")
        s = item.size
        while item.parentId:
            t = (await session.execute(select(Items).where(Items.id == item.parentId))).scalars().first()
            await session.execute(update(Items).where(Items.id == item.parentId).values(date=parser.parse(date),
                                                                                        size=t.size - s if t.size else 0))
            item = t

        query = delete(Items).where(Items.id == id)
        await session.execute(query)

        await session.commit()


@router.get('/nodes/{id}', response_model=SystemItem, status_code=200)
async def get_files(id: str, session: AsyncSession = Depends(get_session)):
    async with session:
        query = select(Items).where(Items.id == id).options(joinedload(Items.children))
        res = await session.execute(query)
        root = res.scalars().first()
        if root is None:
            raise HTTPException(404, detail="Item not found")
        stack = [*root.children]
        while stack:
            cur = stack.pop()
            if not cur:
                continue
            query = select(Items).where(Items.id == cur.id).options(joinedload(Items.children))
            res = await session.execute(query)
            temp = res.scalars().first()
            for i in temp.children:
                stack.append(i)

    return root


@router.get('/updates', response_model=SystemItemHistoryResponse, status_code=200)
async def updates(date: str, session: AsyncSession = Depends(get_session)):
    async with session:
        if not valdate(date):
            raise HTTPException(400, detail="Validation Failed")
        query = select(Items).where(Items.date <= parser.parse(date), Items.date >= parser.parse(date) - timedelta(
            hours=24))  # Items.type is SystemItemType.FILE,
        res = await session.execute(query)
        res = res.scalars().all()
    return res
