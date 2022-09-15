import uvicorn as uvicorn
from fastapi import FastAPI
from fastapi import Request, HTTPException

from starlette.responses import JSONResponse

from app.handlers.items import router as items_router
from app.db.database import engine
from app.schemas.items import Error


def set_events(app: FastAPI):
    @app.on_event("shutdown")
    async def startup_event():
        await engine.dispose()

    @app.exception_handler(HTTPException)
    async def exception(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content=Error(code=exc.status_code, message=exc.detail).dict()
        )


def get_app():
    app = FastAPI(docs_url='/swagger')
    app.include_router(items_router)
    set_events(app)
    return app


if __name__ == '__main__':
    uvicorn.run(get_app(), host='0.0.0.0', port=80)
