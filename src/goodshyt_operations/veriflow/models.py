from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field


TaskType = Literal[
    "equation_creation",
    "data_generation",
    "formula_question_answering",
]


class LinearModelParameters(BaseModel):
    m: float = 3.0
    b: float = 2.0


class ProblemSpec(BaseModel):
    raw_text: str = Field(min_length=1)
    task_type: TaskType
    variables: list[str] = Field(default_factory=lambda: ["x", "y", "m", "b"])
    formula: str = "y = m*x + b"
    parameters: LinearModelParameters = Field(default_factory=LinearModelParameters)
    x_values: list[float] = Field(default_factory=list)
    query_x: float | None = None
    confidence: float = Field(ge=0.0, le=1.0)


class ToolTrace(BaseModel):
    tool_name: str = Field(min_length=1)
    input_data: dict[str, object] = Field(default_factory=dict)
    output_data: dict[str, object] = Field(default_factory=dict)


class ValidationResult(BaseModel):
    is_valid: bool
    checks: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0.0, le=1.0)


class VeriflowResponse(BaseModel):
    spec: ProblemSpec
    rows: list[list[float]] = Field(default_factory=list)
    answer: str | None = None
    steps: list[str] = Field(default_factory=list)
    validation: ValidationResult
    trace: list[ToolTrace] = Field(default_factory=list)
