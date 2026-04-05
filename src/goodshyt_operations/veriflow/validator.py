from __future__ import annotations

from .models import ProblemSpec, ValidationResult


class VeriflowValidator:
    def validate(
        self,
        spec: ProblemSpec,
        rows: list[list[float]],
        answer: str | None,
    ) -> ValidationResult:
        checks: list[str] = []
        is_valid = True

        if spec.task_type == "data_generation":
            for x_value, y_value in rows:
                expected = spec.parameters.m * x_value + spec.parameters.b
                if abs(expected - y_value) > 1e-9:
                    is_valid = False
                    checks.append(f"row failed: x={x_value:g}, expected y={expected:g}, got {y_value:g}")
                else:
                    checks.append(f"row verified: x={x_value:g}, y={y_value:g}")

        if spec.task_type == "formula_question_answering":
            if spec.query_x is None:
                is_valid = False
                checks.append("query_x missing")
            else:
                expected = spec.parameters.m * spec.query_x + spec.parameters.b
                expected_answer = f"When x = {spec.query_x:g}, y = {expected:g}"
                if answer != expected_answer:
                    is_valid = False
                    checks.append("answer text did not match the computed value")
                else:
                    checks.append("answer verified against the linear model")

        if spec.task_type == "equation_creation":
            expected_formula = "y = m*x + b"
            if spec.formula != expected_formula:
                is_valid = False
                checks.append("canonical formula did not match the expected template")
            else:
                checks.append("canonical linear formula verified")

        confidence = spec.confidence if is_valid else max(spec.confidence - 0.4, 0.0)
        return ValidationResult(is_valid=is_valid, checks=checks, confidence=confidence)
