from fastapi import FastAPI
from .models import PlanRequest
from .service import OperationsService

app = FastAPI(title="GoodShyt Operations", version="0.1.0")
service = OperationsService()

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "goodshyt-operations"}

@app.post("/plan")
def plan(payload: PlanRequest) -> dict[str, object]:
    return {"plan": [item.model_dump() for item in service.build_plan(payload)]}

@app.post("/execute")
def execute(payload: PlanRequest) -> dict[str, object]:
    return service.execute(payload).model_dump()
