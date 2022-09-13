from typing import Union
from enum import Enum

import uvicorn as uvicorn
from fastapi import FastAPI, Path
from pydantic import BaseModel
from fastapi import APIRouter
from datetime import datetime
from handlers.items import router as items_router
from app.db.database import async_session, engine


def set_events(app: FastAPI):
    @app.on_event("shutdown")
    async def startup_event():
        await engine.dispose()


def get_app():
    app = FastAPI(docs_url='/swagger')
    app.include_router(items_router)
    set_events(app)
    return app


if __name__ == '__main__':
    uvicorn.run(get_app(), host='0.0.0.0', port=80)
