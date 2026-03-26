"""
Core backend classes for the PawPal+ pet care planning system.

This module is the logic layer for the application. It is intended to hold
the classes and scheduling behavior that the Streamlit UI can call.
"""

from dataclasses import dataclass, field


@dataclass
class Owner:
    name: str
    available_time_minutes: int
    preferences: str = ""
    pets: list["Pet"] = field(default_factory=list)

    def set_available_time(self, minutes: int) -> None:
        """Update the owner's available time for pet care."""
        pass

    def update_preferences(self, preferences: str) -> None:
        """Update the owner's care preferences."""
        pass

    def add_pet(self, pet: "Pet") -> None:
        """Associate a pet with this owner."""
        pass


@dataclass
class Pet:
    name: str
    species: str

    def update_info(self, name: str, species: str) -> None:
        """Update the pet's basic information."""
        pass

    def get_summary(self) -> str:
        """Return a short summary of the pet."""
        pass


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str

    def update_task(self, title: str, duration_minutes: int, priority: str) -> None:
        """Update the task details."""
        pass

    def get_priority_value(self) -> int:
        """Convert the task priority into a comparable numeric value."""
        pass


class Scheduler:
    def __init__(self, owner: Owner, pet: Pet, task_list: list[Task]) -> None:
        self.owner = owner
        self.pet = pet
        self.task_list = task_list

    def generate_schedule(self) -> list[Task]:
        """Create a daily schedule from the available tasks."""
        pass

    def sort_tasks_by_priority(self) -> list[Task]:
        """Sort tasks based on priority."""
        pass

    def filter_tasks_by_time(self) -> list[Task]:
        """Select tasks that fit within the owner's available time."""
        pass
