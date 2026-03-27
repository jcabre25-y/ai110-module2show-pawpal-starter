from datetime import date, timedelta

from pawpal_system import Owner, Pet, Scheduler, Task


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


def test_sort_by_time_returns_tasks_in_chronological_order() -> None:
    owner = Owner(name="Jordan", available_time_minutes=60)
    mochi = Pet(name="Mochi", species="dog")
    today = date.today()

    mochi.add_task(
        Task(
            description="Evening walk",
            duration_minutes=20,
            frequency="daily",
            time="18:00",
            due_date=today,
            priority="high",
        )
    )
    mochi.add_task(
        Task(
            description="Breakfast",
            duration_minutes=10,
            frequency="daily",
            time="07:30",
            due_date=today,
            priority="high",
        )
    )
    mochi.add_task(
        Task(
            description="Vet reminder",
            duration_minutes=5,
            frequency="weekly",
            time="09:00",
            due_date=today + timedelta(days=1),
            priority="medium",
        )
    )

    owner.add_pet(mochi)
    scheduler = Scheduler(owner)

    sorted_tasks = scheduler.sort_by_time(scheduler.retrieve_all_tasks())

    assert [task.description for _, task in sorted_tasks] == [
        "Breakfast",
        "Evening walk",
        "Vet reminder",
    ]


def test_mark_task_complete_creates_next_daily_task() -> None:
    owner = Owner(name="Jordan", available_time_minutes=60)
    pet = Pet(name="Mochi", species="dog")
    today = date.today()
    pet.add_task(
        Task(
            description="Morning walk",
            duration_minutes=20,
            frequency="daily",
            time="08:00",
            due_date=today,
            priority="high",
        )
    )
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    was_marked = scheduler.mark_task_complete("Mochi", "Morning walk")

    assert was_marked is True
    assert len(pet.tasks) == 2
    assert pet.tasks[0].completed is True
    assert pet.tasks[1].completed is False
    assert pet.tasks[1].due_date == today + timedelta(days=1)


def test_mark_task_complete_creates_next_weekly_task() -> None:
    owner = Owner(name="Jordan", available_time_minutes=60)
    pet = Pet(name="Luna", species="cat")
    today = date.today()
    pet.add_task(
        Task(
            description="Weigh-in",
            duration_minutes=10,
            frequency="weekly",
            time="10:30",
            due_date=today,
            priority="medium",
        )
    )
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    scheduler.mark_task_complete("Luna", "Weigh-in")

    assert len(pet.tasks) == 2
    assert pet.tasks[1].due_date == today + timedelta(weeks=1)


def test_mark_task_complete_does_not_clone_non_recurring_task() -> None:
    owner = Owner(name="Jordan", available_time_minutes=60)
    pet = Pet(name="Luna", species="cat")
    pet.add_task(
        Task(
            description="Bath",
            duration_minutes=30,
            frequency="as needed",
            time="14:00",
            priority="low",
        )
    )
    owner.add_pet(pet)
    scheduler = Scheduler(owner)

    scheduler.mark_task_complete("Luna", "Bath")

    assert len(pet.tasks) == 1
    assert pet.tasks[0].completed is True


def test_detect_conflicts_returns_warning_message() -> None:
    owner = Owner(name="Jordan", available_time_minutes=60)
    mochi = Pet(name="Mochi", species="dog")
    luna = Pet(name="Luna", species="cat")
    today = date.today()

    mochi.add_task(
        Task(
            description="Evening walk",
            duration_minutes=20,
            frequency="daily",
            time="18:00",
            due_date=today,
            priority="high",
        )
    )
    luna.add_task(
        Task(
            description="Feed dinner",
            duration_minutes=10,
            frequency="daily",
            time="18:00",
            due_date=today,
            priority="medium",
        )
    )

    owner.add_pet(mochi)
    owner.add_pet(luna)
    scheduler = Scheduler(owner)

    warnings = scheduler.detect_conflicts()

    assert len(warnings) == 1
    assert "Warning: conflict detected" in warnings[0]
    assert "Evening walk" in warnings[0]
    assert "Feed dinner" in warnings[0]
