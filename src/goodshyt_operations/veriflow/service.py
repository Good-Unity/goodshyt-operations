from __future__ import annotations

from .models import ProblemSpec, ToolTrace, VeriflowResponse
from .planner import VeriflowPlanner
from .tools import answer_linear_query, generate_linear_rows
from .validator import VeriflowValidator


class VeriflowService:
    def __init__(self) -> None:
        self._planner = VeriflowPlanner()
        self._validator = VeriflowValidator()

    def parse(self, text: str) -> VeriflowResponse:
        spec, trace = self._parse_spec(text)
        validation = self._validator.validate(spec=spec, rows=[], answer=None)
        return VeriflowResponse(
            spec=spec,
            rows=[],
            answer=f"Created equation: {spec.formula}",
            steps=["Parsed request into the canonical linear-model template."],
            validation=validation,
            trace=trace,
        )

    def generate_data(self, text: str) -> VeriflowResponse:
        spec, trace = self._parse_spec(text)
        rows, steps = generate_linear_rows(spec.parameters, spec.x_values)
        trace.append(
            ToolTrace(
                tool_name="generate_linear_rows",
                input_data={"formula": spec.formula, "x_values": spec.x_values},
                output_data={"rows": rows},
            )
        )
        validation = self._validator.validate(spec=spec, rows=rows, answer=None)
        return VeriflowResponse(
            spec=spec,
            rows=rows,
            answer=f"Generated {len(rows)} rows from {spec.formula}",
            steps=steps,
            validation=validation,
            trace=trace,
        )

    def answer(self, text: str) -> VeriflowResponse:
        spec, trace = self._parse_spec(text)
        query_x = 10.0 if spec.query_x is None else spec.query_x
        spec = ProblemSpec(**{**spec.model_dump(), "query_x": query_x})
        answer, steps = answer_linear_query(spec.parameters, query_x)
        trace.append(
            ToolTrace(
                tool_name="answer_linear_query",
                input_data={"formula": spec.formula, "x": query_x},
                output_data={"answer": answer},
            )
        )
        validation = self._validator.validate(spec=spec, rows=[], answer=answer)
        return VeriflowResponse(
            spec=spec,
            rows=[],
            answer=answer,
            steps=steps,
            validation=validation,
            trace=trace,
        )

    def run(self, text: str) -> VeriflowResponse:
        spec = self._planner.parse_request(text)
        if spec.task_type == "data_generation":
            return self.generate_data(text)
        if spec.task_type == "formula_question_answering":
            return self.answer(text)
        return self.parse(text)

    def _parse_spec(self, text: str) -> tuple[ProblemSpec, list[ToolTrace]]:
        spec = self._planner.parse_request(text)
        trace = [
            ToolTrace(
                tool_name="parse_request",
                input_data={"text": text},
                output_data=spec.model_dump(),
            )
        ]
        return spec, trace
