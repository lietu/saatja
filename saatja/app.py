from fastapi import FastAPI, Request

from saatja.api.scheduler import scheduler_router
from saatja.api.task import task_router
from saatja.db.utils import configure_db
from saatja.log import gcloud_logging_middleware

app = FastAPI(title="Saatja webhook delivery system", version="1.0.0")
app.include_router(task_router, prefix="/task")
app.include_router(scheduler_router, prefix="/scheduler")
app.middleware("http")(gcloud_logging_middleware)


@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "31536000"  # 1 year
    return response


@app.on_event("startup")
def initialize():
    configure_db()
