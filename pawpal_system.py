"""
Core backend classes for the PawPal+ pet care planning system.

This module provides the application logic independently from the Streamlit UI.
"""

from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class Task:
    description: str
    duration_minutes: int
    frequency: str
    priority: str = "medium"
    completed: bool = False
    PRIORITY_VALUES: ClassVar[dict[str, int]] = {"high": 3, "medium": 2, "low": 1}

    def mark_complete(self) -> None:
        """Mark the task as complete."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark the task as incomplete."""
        self.completed = False

    def update_details(
        self,
        description: str,
        duration_minutes: int,
        frequency: str,
        priority: str,
    ) -> None:
        """Update the task details."""
        self.description = description
        self.duration_minutes = duration_minutes
        self.frequency = frequency
        self.priority = priority

    def get_priority_value(self) -> int:
        """Convert the priority label into a numeric ranking."""
        return self.PRIORITY_VALUES.get(self.priority.lower(), 0)


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task for this pet."""
        self.tasks.append(task)

    def remove_task(self, task_description: str) -> bool:
        """Remove a task by description if it exists."""
        for task in self.tasks:
            if task.description == task_description:
                self.tasks.remove(task)
                return True
        return False

    def get_tasks(self) -> list[Task]:
        """Return all tasks for this pet."""
        return self.tasks

    def update_info(self, name: str, species: str) -> None:
        """Update the pet's basic information."""
        self.name = name
        self.species = species

    def get_summary(self) -> str:
        """Return a short summary of the pet and task count."""
        return f"{self.name} is a {self.species} with {len(self.tasks)} care task(s)."


@dataclass
class Owner:
    name: str
    available_time_minutes: int
    preferences: str = ""
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's care list."""
        self.pets.append(pet)

    def remove_pet(self, pet_name: str) -> bool:
        """Remove a pet by name if it exists."""
        for pet in self.pets:
            if pet.name == pet_name:
                self.pets.remove(pet)
                return True
        return False

    def get_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Return every task paired with the pet it belongs to."""
        pet_tasks: list[tuple[Pet, Task]] = []
        for pet in self.pets:
            for task in pet.get_tasks():
                pet_tasks.append((pet, task))
        return pet_tasks

    def set_available_time(self, minutes: int) -> None:
        """Update the owner's available time for pet care."""
        self.available_time_minutes = minutes

    def update_preferences(self, preferences: str) -> None:
        """Update the owner's care preferences."""
        self.preferences = preferences


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        """Initialize the scheduler with the owner's pet data."""
        self.owner = owner

    def retrieve_all_tasks(self) -> list[tuple[Pet, Task]]:
        """Get all tasks across the owner's pets."""
        return self.owner.get_all_tasks()

    def get_incomplete_tasks(self) -> list[tuple[Pet, Task]]:
        """Return only tasks that still need to be done."""
        return [
            (pet, task)
            for pet, task in self.retrieve_all_tasks()
            if not task.completed
        ]

    def sort_tasks_by_priority(self, tasks: list[tuple[Pet, Task]]) -> list[tuple[Pet, Task]]:
        """Sort tasks by priority, then by shortest duration."""
        return sorted(
            tasks,
            key=lambda pet_task: (
                pet_task[1].get_priority_value(),
                -pet_task[1].duration_minutes,
            ),
            reverse=True,
        )

    def build_daily_plan(self) -> list[tuple[Pet, Task]]:
        """Build a simple schedule that fits within the owner's available time."""
        sorted_tasks = self.sort_tasks_by_priority(self.get_incomplete_tasks())
        daily_plan: list[tuple[Pet, Task]] = []
        remaining_minutes = self.owner.available_time_minutes

        for pet, task in sorted_tasks:
            if task.duration_minutes <= remaining_minutes:
                daily_plan.append((pet, task))
                remaining_minutes -= task.duration_minutes

        return daily_plan

    def mark_task_complete(self, pet_name: str, task_description: str) -> bool:
        """Mark a specific pet task as complete."""
        for pet, task in self.retrieve_all_tasks():
            if pet.name == pet_name and task.description == task_description:
                task.mark_complete()
                return True
        return False

    def get_plan_summary(self) -> list[str]:
        """Return readable schedule lines for display or CLI output."""
        summary_lines: list[str] = []
        for pet, task in self.build_daily_plan():
            summary_lines.append(
                f"{pet.name}: {task.description} ({task.duration_minutes} min, "
                f"{task.frequency}, {task.priority} priority)"
            )
        return summary_lines


if __name__ == "__main__":
    owner = Owner(name="Jordan", available_time_minutes=60, preferences="Prefers morning care")

    mochi = Pet(name="Mochi", species="dog")
    mochi.add_task(Task(description="Morning walk", duration_minutes=20, frequency="daily", priority="high"))
    mochi.add_task(Task(description="Breakfast", duration_minutes=10, frequency="daily", priority="high"))

    luna = Pet(name="Luna", species="cat")
    luna.add_task(Task(description="Litter box cleaning", duration_minutes=10, frequency="daily", priority="medium"))
    luna.add_task(Task(description="Play session", duration_minutes=15, frequency="daily", priority="low"))

    owner.add_pet(mochi)
    owner.add_pet(luna)

    scheduler = Scheduler(owner)

    print(f"Daily plan for {owner.name}:")
    for line in scheduler.get_plan_summary():
        print(f"- {line}")
