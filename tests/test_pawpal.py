from pawpal_system import Pet, Task


def test_mark_complete_sets_task_status_to_true() -> None:
    task = Task(
        description="Give medication",
        duration_minutes=5,
        frequency="daily",
        priority="high",
    )

    task.mark_complete()

    assert task.completed is True


def test_adding_task_to_pet_increases_task_count() -> None:
    pet = Pet(name="Mochi", species="dog")
    starting_count = len(pet.tasks)

    pet.add_task(
        Task(
            description="Evening walk",
            duration_minutes=20,
            frequency="daily",
            priority="medium",
        )
    )

    assert len(pet.tasks) == starting_count + 1
