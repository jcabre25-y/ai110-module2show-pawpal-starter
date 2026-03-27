import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


def get_pet_by_name(owner: Owner, pet_name: str) -> Pet | None:
    """Return the matching pet object for a given pet name."""
    for pet in owner.pets:
        if pet.name == pet_name:
            return pet
    return None


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
This version is now connected to the backend classes in `pawpal_system.py`.
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
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=1)

    if st.button("Add task"):
        selected_pet = get_pet_by_name(owner, selected_pet_name)
        if selected_pet is None:
            st.error("Choose a valid pet before adding a task.")
        elif not task_description.strip():
            st.error("Enter a task description before adding a task.")
        else:
            selected_pet.add_task(
                Task(
                    description=task_description.strip(),
                    duration_minutes=int(duration),
                    frequency=frequency,
                    priority=priority,
                )
            )
            st.success(f"Added task to {selected_pet.name}.")

    st.markdown("### Saved tasks")
    for pet in owner.pets:
        if pet.tasks:
            st.write(f"**{pet.name}**")
            for task in pet.tasks:
                st.write(
                    f"- {task.description} | {task.duration_minutes} min | "
                    f"{task.frequency} | {task.priority} priority"
                )
        else:
            st.write(f"**{pet.name}**")
            st.caption("No tasks yet.")

st.divider()

st.subheader("Today's Schedule")

if st.button("Generate schedule"):
    scheduler = Scheduler(owner)
    daily_plan = scheduler.build_daily_plan()

    if not daily_plan:
        st.warning("No tasks fit into today's schedule yet.")
    else:
        st.success("Schedule generated.")
        total_minutes = 0
        for index, (pet, task) in enumerate(daily_plan, start=1):
            total_minutes += task.duration_minutes
            st.write(
                f"{index}. {pet.name} - {task.description} "
                f"({task.duration_minutes} min, {task.priority} priority)"
            )
        st.caption(f"Total scheduled time: {total_minutes} minutes")
