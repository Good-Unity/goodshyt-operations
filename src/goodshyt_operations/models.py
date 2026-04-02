from typing import Literal
from pydantic import BaseModel, Field

TaskStatus = Literal["planned", "blocked", "executed"]

class Task(BaseModel):
    task_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    priority: int = Field(ge=1, le=5)
    required_staff: int = Field(ge=1)
    estimated_minutes: int = Field(ge=1)
    dependencies: list[str] = []

class PlanRequest(BaseModel):
    shift_name: str
    available_staff: int = Field(ge=1)
    tasks: list[Task]

class PlannedTask(BaseModel):
    task_id: str
    title: str
    status: TaskStatus
    reason: str = ""

class ExecutionSummary(BaseModel):
    shift_name: str
    executed: list[str]
    blocked: list[str]
    total_minutes: int
