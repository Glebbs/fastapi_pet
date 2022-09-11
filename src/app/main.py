from typing import Union
from enum import Enum

import uvicorn as uvicorn
from fastapi import FastAPI, Path
from pydantic import BaseModel
from fastapi import APIRouter
from datetime import datetime
from handlers.items import router as items_router


def get_app():
    app = FastAPI(docs_url='/swagger')
    app.include_router(items_router)
    return app

if __name__ == '__main__':
    uvicorn.run(get_app(), host='0.0.0.0', port=80)