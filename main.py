from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(
        name="Jordan",
        available_time_minutes=65,
        preferences="Prefers to finish the highest-priority pet care first.",
    )

    mochi = Pet(name="Mochi", species="dog")
    mochi.add_task(
        Task(
            description="Evening walk",
            duration_minutes=20,
            frequency="daily",
            time="18:00",
            due_date=date.today(),
            priority="high",
        )
    )
    mochi.add_task(
        Task(
            description="Breakfast",
            duration_minutes=10,
            frequency="daily",
            time="07:30",
            due_date=date.today(),
            priority="high",
        )
    )

    luna = Pet(name="Luna", species="cat")
    luna.add_task(
        Task(
            description="Play session",
            duration_minutes=15,
            frequency="daily",
            time="19:15",
            due_date=date.today(),
            priority="low",
        )
    )
    luna.add_task(
        Task(
            description="Feed dinner",
            duration_minutes=10,
            frequency="daily",
            time="18:00",
            due_date=date.today(),
            priority="medium",
        )
    )
    luna.add_task(
        Task(
            description="Morning medication",
            duration_minutes=5,
            frequency="daily",
            time="08:15",
            due_date=date.today(),
            priority="high",
        )
    )

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)
    scheduler.mark_task_complete("Luna", "Play session")
    all_tasks = scheduler.retrieve_all_tasks()
    sorted_tasks = scheduler.sort_by_time(all_tasks)
    pending_tasks = scheduler.filter_tasks(completed=False)
    luna_tasks = scheduler.filter_tasks(pet_name="Luna")
    conflict_warnings = scheduler.detect_conflicts()

    print("Task Sorting, Filtering, Recurrence, and Conflicts Demo")
    print("=======================================================")
    print(f"Owner: {owner.name}")
    print(f"Available time: {owner.available_time_minutes} minutes")
    print()

    print("Conflict warnings")
    if conflict_warnings:
        for warning in conflict_warnings:
            print(warning)
    else:
        print("No scheduling conflicts detected.")

    print()
    print("Tasks sorted by time")
    for index, (pet, task) in enumerate(sorted_tasks, start=1):
        status = "complete" if task.completed else "pending"
        print(
            f"{index}. {task.due_date.isoformat()} {task.time} | {pet.name} ({pet.species})"
            f" - {task.description}"
            f" | {task.duration_minutes} min"
            f" | {task.priority} priority"
            f" | {status}"
        )

    print()
    print("Pending tasks only")
    for index, (pet, task) in enumerate(pending_tasks, start=1):
        print(
            f"{index}. {task.due_date.isoformat()} {task.time} | {pet.name}"
            f" - {task.description}"
        )

    print()
    print("Tasks filtered to Luna")
    for index, (pet, task) in enumerate(luna_tasks, start=1):
        status = "complete" if task.completed else "pending"
        print(
            f"{index}. {task.due_date.isoformat()} {task.time} | {pet.name}"
            f" - {task.description}"
            f" | {status}"
        )


if __name__ == "__main__":
    main()
