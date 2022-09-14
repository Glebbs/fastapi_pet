from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, update, select, insert
from sqlalchemy.orm import joinedload

from app.schemas import SystemItemImportRequest, SystemItemType, SystemItem
from datetime import datetime
from app.db.database import get_session
from app.db.models import Items

router = APIRouter(tags=['Базовые задачи'])


@router.post('/imports')
async def import_files(model: SystemItemImportRequest,
                       session: AsyncSession = Depends(get_session)):
    async with session:
        for item in model.items:
            query = insert(Items).values(**item.dict(exclude_none=True), date=model.updateDate.replace(tzinfo=None))
            await session.execute(query)

        query = select(Items)#.where(Items.type is SystemItemType.FILE)
        res = (await session.execute(query)).scalars().all()
        print(res)
        for item in model.items:
            print(item.id, item.type)
            if item.type.value != 'FILE':
                continue
            s = item.size
            while item.parentId:
                t = (await session.execute(select(Items).where(Items.id == item.parentId))).scalars().first()
                await session.execute(update(Items).where(Items.id == item.parentId).values(
                    size=t.size + s if t.size else s))
                item = t
        await session.commit()

    return


@router.delete('/delete/{id}')
async def delete_files(date: datetime, id: str, session: AsyncSession = Depends(get_session)):
    async with session:
        query = select(Items).where(Items.id == id)
        res = (await session.execute(query)).scalars().first()
        par = (await session.execute(select(Items).where(Items.id == res.parentId))).scalars().first()

        if par:
            query = update(Items).where(Items.id == res.parentId).values(date=date.replace(tzinfo=None),
                                                                         size=par.size - res.size)
        await session.execute(query)

        query = delete(Items).where(Items.id == id)
        await session.execute(query)

        await session.commit()
    return


@router.get('/nodes/{id}', response_model=SystemItem)
async def get_files(id: str, session: AsyncSession = Depends(get_session)):
    async with session:
        query = select(Items).where(Items.id == id).options(joinedload(Items.children))
        res = await session.execute(query)
        root = res.scalars().first()

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


@router.get('/updates', response_model=SystemItem)
async def updates(date: datetime, session: AsyncSession = Depends(get_session)):
    async with session:
        query = select(Items).where().options(joinedload(Items.children))
        res = await session.execute(query)
        root = res.scalars().all()

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

# {
#   "items": [
#     {
#       "id": "элемент_1",
#       "size": 0,
#       "type": "FOLDER"
#     },
#     {
#       "id": "элемент_1_1",
#       "url": "/file/url1",
#       "parentId": "элемент_1",
#       "size": 45,
#       "type": "FILE"
#     },
#     {
#       "id": "элемент_1_2",
#       "parentId": "элемент_1",
#       "size": 0,
#       "type": "FOLDER"
#     },
#     {
#       "id": "элемент_1_2_1",
#       "url": "/file/url3",
#       "parentId": "элемент_1_2",
#       "size": 234,
#       "type": "FILE"
#     },
#     {
#       "id": "элемент_1_2_3",
#       "parentId": "элемент_1_2",
#       "size": 100,
#       "type": "FOLDER"
#     }
#   ],
#   "updateDate": "2022-05-28T21:12:01.000Z"
# }


# {
#   "items": [
#     {
#       "id": "1",
#       "type": "FOLDER"
#     },
#     {
#       "id": "2",
#       "parentId": "1",
#       "type": "FOLDER"
#     },
# {
#       "id": "3",
#       "parentId": "2",
#       "type": "FOLDER"
#     },
# {
#       "id": "4",
#       "parentId": "3",
#       "type": "FOLDER"
#     },
#     {
#       "id": "5",
#       "parentId": "4",
#       "type": "FOLDER"
#     },
#     {
#       "id": "10",
#       "url": "/file/url3",
#       "parentId": "5",
#       "size": 234,
#       "type": "FILE"
#     }
#   ],
#   "updateDate": "2022-05-28T21:12:01.000Z"
# }


# {
#   "items": [
#     {
#       "id": "11",
#       "url": "/file/url1",
#       "parentId": "3",
#       "size": 1,
#       "type": "FILE"
#     }
#   ],
#   "updateDate": "2022-05-28T21:12:01.000Z"
# }
