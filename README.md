# PawPal+ (Module 2 Project)

**PawPal+** is a Streamlit app that helps a pet owner organize care tasks, build a smarter daily schedule, and review useful scheduling warnings before the day begins.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Features

- Owner and pet setup for multi-pet scheduling.
- Task creation with duration, priority, frequency, due date, and start time.
- Sorting by due date and time for a clearer schedule view.
- Filtering by pet name and completion status.
- Daily and weekly recurrence that automatically creates the next task occurrence when a recurring task is completed.
- Conflict warnings for exact same-date, same-time tasks.
- Daily plan generation based on available time and task priority.
- Automated tests for core scheduling logic.

## 📸 Demo

<a href="/course_images/ai110/pawpal_final_demo.png" target="_blank"><img src='/course_images/ai110/pawpal_final_demo.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>

## Smarter Scheduling

PawPal+ now includes a smarter scheduler with a few practical planning features:

- Tasks can be sorted by due date and time so the daily schedule is easier to follow.
- Tasks can be filtered by pet name or completion status for quick review.
- Daily and weekly recurring tasks automatically create the next occurrence when completed.
- The scheduler can detect lightweight scheduling conflicts and return warning messages when two tasks are set for the same time.

## Testing PawPal+

Run the automated test suite with:

```bash
python -m pytest
```

The tests cover core scheduler behavior, including task completion, chronological sorting, recurring task creation for daily and weekly tasks, and conflict detection for duplicate task times.

Confidence Level: 4/5 stars based on the current automated test results. The core scheduling logic is behaving reliably in the tested scenarios, but more edge cases and UI-level tests would improve confidence further.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
