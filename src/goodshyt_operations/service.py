from .models import ExecutionSummary, PlanRequest, PlannedTask

class OperationsService:
    def build_plan(self, payload: PlanRequest) -> list[PlannedTask]:
        completed: set[str] = set()
        plan: list[PlannedTask] = []
        ordered = sorted(payload.tasks, key=lambda t: (t.priority, t.estimated_minutes))
        for task in ordered:
            if task.required_staff > payload.available_staff:
                plan.append(PlannedTask(task_id=task.task_id, title=task.title, status="blocked", reason="insufficient staff"))
                continue
            unmet = [dep for dep in task.dependencies if dep not in completed]
            if unmet:
                plan.append(PlannedTask(task_id=task.task_id, title=task.title, status="blocked", reason=f"unmet dependencies: {', '.join(unmet)}"))
                continue
            plan.append(PlannedTask(task_id=task.task_id, title=task.title, status="planned"))
            completed.add(task.task_id)
        return plan

    def execute(self, payload: PlanRequest) -> ExecutionSummary:
        plan = self.build_plan(payload)
        executed = [task.task_id for task in plan if task.status == "planned"]
        blocked = [task.task_id for task in plan if task.status == "blocked"]
        total_minutes = sum(task.estimated_minutes for task in payload.tasks if task.task_id in executed)
        return ExecutionSummary(shift_name=payload.shift_name, executed=executed, blocked=blocked, total_minutes=total_minutes)
