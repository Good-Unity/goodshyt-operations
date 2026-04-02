from goodshyt_operations.models import PlanRequest, Task
from goodshyt_operations.service import OperationsService


def test_blocked_when_staff_is_too_low() -> None:
    service = OperationsService()
    payload = PlanRequest(
        shift_name="dinner",
        available_staff=1,
        tasks=[Task(task_id="kitchen", title="Kitchen Prep", priority=1, required_staff=2, estimated_minutes=30)],
    )
    plan = service.build_plan(payload)
    assert plan[0].status == "blocked"


def test_dependencies_affect_execution() -> None:
    service = OperationsService()
    payload = PlanRequest(
        shift_name="event",
        available_staff=3,
        tasks=[
            Task(task_id="setup", title="Setup", priority=1, required_staff=2, estimated_minutes=20),
            Task(task_id="serve", title="Serve Guests", priority=2, required_staff=2, estimated_minutes=60, dependencies=["setup"]),
        ],
    )
    result = service.execute(payload)
    assert result.executed == ["setup", "serve"]
