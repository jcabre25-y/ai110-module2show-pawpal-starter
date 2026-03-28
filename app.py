from datetime import date
from typing import Optional

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


def get_pet_by_name(owner: Owner, pet_name: str) -> Optional[Pet]:
    """Return the matching pet object for a given pet name."""
    for pet in owner.pets:
        if pet.name == pet_name:
            return pet
    return None


def build_task_rows(tasks: list[tuple[Pet, Task]]) -> list[dict[str, object]]:
    """Convert scheduled tasks into rows for Streamlit tables."""
    rows: list[dict[str, str | int]] = []
    for pet, task in tasks:
        rows.append(
            {
                "Pet": pet.name,
                "Species": pet.species,
                "Task": task.description,
                "Due Date": task.due_date.isoformat(),
                "Time": task.time,
                "Duration (min)": task.duration_minutes,
                "Frequency": task.frequency,
                "Priority": task.priority.title(),
                "Status": "Complete" if task.completed else "Pending",
            }
        )
    return rows


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name="Jordan",
        available_time_minutes=60,
        preferences="",
    )

owner = st.session_state.owner

st.title("🐾 PawPal+")

st.markdown(
    """
PawPal+ helps a pet owner keep track of care tasks and build a daily plan.
This version uses the smart scheduling logic in `pawpal_system.py` to sort tasks,
filter the schedule, surface conflicts, and support recurring care tasks.
"""
)

st.subheader("Owner Setup")
owner_name = st.text_input("Owner name", value=owner.name)
available_time = st.number_input(
    "Available time today (minutes)",
    min_value=1,
    max_value=480,
    value=owner.available_time_minutes,
)
preferences = st.text_input("Owner preferences", value=owner.preferences)

owner.name = owner_name
owner.set_available_time(int(available_time))
owner.update_preferences(preferences)

st.divider()

st.subheader("Add a Pet")
pet_name = st.text_input("Pet name", value="")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    if not pet_name.strip():
        st.error("Enter a pet name before adding a pet.")
    elif get_pet_by_name(owner, pet_name.strip()) is not None:
        st.warning("That pet already exists in this session.")
    else:
        owner.add_pet(Pet(name=pet_name.strip(), species=species))
        st.success(f"Added {pet_name.strip()} to {owner.name}'s pets.")

if owner.pets:
    st.markdown("### Current pets")
    for pet in owner.pets:
        st.write(f"- {pet.get_summary()}")
else:
    st.info("No pets added yet.")

st.divider()

st.subheader("Add a Task")

if not owner.pets:
    st.info("Add a pet first before creating tasks.")
else:
    pet_options = [pet.name for pet in owner.pets]
    selected_pet_name = st.selectbox("Choose a pet", pet_options)
    task_description = st.text_input("Task description", value="Morning walk")
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"])
    due_date = st.date_input("Due date", value=date.today())
    task_time = st.text_input("Start time (HH:MM)", value="09:00")
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)

    if st.button("Add task"):
        selected_pet = get_pet_by_name(owner, selected_pet_name)
        if selected_pet is None:
            st.error("Choose a valid pet before adding a task.")
        elif not task_description.strip():
            st.error("Enter a task description before adding a task.")
        elif len(task_time) != 5 or task_time[2] != ":":
            st.error("Enter the task time in HH:MM format, like 08:30.")
        else:
            selected_pet.add_task(
                Task(
                    description=task_description.strip(),
                    duration_minutes=int(duration),
                    frequency=frequency,
                    time=task_time,
                    due_date=due_date,
                    priority=priority,
                )
            )
            st.success(f"Added task to {selected_pet.name}.")

    st.markdown("### Saved tasks")
    scheduler = Scheduler(owner)
    all_tasks = scheduler.sort_by_time(scheduler.retrieve_all_tasks())
    if all_tasks:
        st.table(build_task_rows(all_tasks))
    else:
        st.caption("No tasks yet.")

st.divider()

st.subheader("Smart Schedule")

if owner.pets:
    scheduler = Scheduler(owner)
    pet_filter = st.selectbox("Filter by pet", ["All pets"] + [pet.name for pet in owner.pets])
    status_filter = st.selectbox("Filter by status", ["All", "Pending", "Complete"])

    filtered_tasks = scheduler.retrieve_all_tasks()
    if pet_filter != "All pets":
        filtered_tasks = scheduler.filter_tasks(pet_name=pet_filter)

    if status_filter != "All":
        filtered_tasks = scheduler.filter_tasks(
            completed=status_filter == "Complete",
            pet_name=None if pet_filter == "All pets" else pet_filter,
        )

    sorted_filtered_tasks = scheduler.sort_by_time(filtered_tasks)
    conflict_warnings = scheduler.detect_conflicts(sorted_filtered_tasks)

    if conflict_warnings:
        st.warning(
            "Scheduling conflict detected. Review the tasks below before following today's plan."
        )
        for warning in conflict_warnings:
            st.warning(warning)
    else:
        st.success("No exact-time conflicts detected in the current schedule.")

    if sorted_filtered_tasks:
        st.markdown("### Sorted and filtered task list")
        st.table(build_task_rows(sorted_filtered_tasks))
    else:
        st.info("No tasks match the selected filters yet.")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    daily_plan = scheduler.build_daily_plan()

    if not daily_plan:
        st.warning("No tasks fit into today's schedule yet.")
    else:
        st.success("Schedule generated.")
        st.table(build_task_rows(daily_plan))
        total_minutes = 0
        for index, (pet, task) in enumerate(daily_plan, start=1):
            total_minutes += task.duration_minutes
            st.write(
                f"{index}. {task.time} | {pet.name} - {task.description} "
                f"({task.duration_minutes} min, due {task.due_date.isoformat()}, "
                f"{task.priority} priority)"
            )
        st.caption(f"Total scheduled time: {total_minutes} minutes")
