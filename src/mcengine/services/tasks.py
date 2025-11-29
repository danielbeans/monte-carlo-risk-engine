import time


def test_task(task_id: str) -> None:
    """Test task for RQ worker."""
    print(f"Test task {task_id} started")
    time.sleep(10)
    print(f"Test task {task_id} completed")
