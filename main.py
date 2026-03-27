from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(
        name="Jordan",
        available_time_minutes=65,
        preferences="Prefers to finish the highest-priority pet care first.",
    )

    mochi = Pet(name="Mochi", species="dog")
    mochi.add_task(Task(description="Morning walk", duration_minutes=20, frequency="daily", priority="high"))
    mochi.add_task(Task(description="Breakfast", duration_minutes=10, frequency="daily", priority="high"))

    luna = Pet(name="Luna", species="cat")
    luna.add_task(Task(description="Feed dinner", duration_minutes=10, frequency="daily", priority="medium"))
    luna.add_task(Task(description="Play session", duration_minutes=15, frequency="daily", priority="low"))

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)
    daily_plan = scheduler.build_daily_plan()

    print("Today's Schedule")
    print("================")
    print(f"Owner: {owner.name}")
    print(f"Available time: {owner.available_time_minutes} minutes")
    print()

    if not daily_plan:
        print("No tasks fit into today's available time.")
        return

    total_minutes = 0
    for index, (pet, task) in enumerate(daily_plan, start=1):
        total_minutes += task.duration_minutes
        print(
            f"{index}. {pet.name} ({pet.species})"
            f" - {task.description}"
            f" | {task.duration_minutes} min"
            f" | {task.frequency}"
            f" | {task.priority} priority"
        )

    print()
    print(f"Total scheduled time: {total_minutes} minutes")


if __name__ == "__main__":
    main()
