# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial design focused on three main actions the user should be able to perform in the app. First, the user should be able to add and manage pet and owner information so the system knows who the schedule is for and can consider basic preferences. Second, the user should be able to create and update pet care tasks such as feeding, walking, medication, grooming, and enrichment, including details like duration and priority. Third, the user should be able to generate and review a daily care schedule that selects tasks based on the available time and priorities, then clearly shows the order of tasks and the reasoning behind the plan.

To support those actions, I chose four main classes: `Owner`, `Pet`, `Task`, and `Scheduler`. The `Owner` class is responsible for storing information about the pet owner, including their name, available time, and general care preferences. The `Pet` class stores basic information about the animal, such as its name and species. The `Task` class represents an individual care activity and holds details like the task title, duration, and priority. The `Scheduler` class is responsible for the planning logic. It takes the owner, pet, and task information and uses it to organize tasks into a daily care schedule. I chose these classes because they separate the data from the scheduling behavior and make the system easier to understand and build.

**b. Design changes**

My design changed in two important ways as the project became more complete. First, I ended up keeping support for multiple pets instead of simplifying to a single-pet system. In the final version, the `Owner` stores a list of pets, each `Pet` stores its own tasks, and the `Scheduler` works across all of them by retrieving `(pet, task)` pairs. That change made the app more realistic and also made filtering and conflict detection more meaningful because the scheduler can compare tasks across pets.

Second, the `Task` class became richer than my original sketch. At first I mainly planned for a description, duration, and priority. In the final version, `Task` also includes `time`, `due_date`, and recurring behavior through `create_next_occurrence()`. The `Scheduler` also gained more specialized methods such as sorting by time, filtering, recurring task rollover, and conflict detection. These additions made the design less minimal than the original UML, but they made the system much closer to a real scheduling tool.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

My scheduler considers several constraints. The main ones are the owner's available time, each task's duration, each task's priority, whether a task is already completed, and when the task is due. It also tracks the scheduled start time for sorting and checks for exact-time conflicts so the user can see when two tasks are set for the same moment. For recurring tasks, the scheduler also considers frequency so daily and weekly tasks automatically roll forward after completion.

I decided these constraints mattered most because they directly affect whether a daily plan is practical. Available time and duration determine whether a task can fit into the day at all. Priority matters because some pet care tasks, like medication or feeding, should be chosen before lower-priority enrichment tasks when time is limited. Due date and time matter because a schedule is more useful if it is presented in chronological order. I treated owner preferences as supporting context rather than a fully implemented scheduling rule, because I wanted to keep the first version understandable and make sure the core planning logic worked reliably first.

**b. Tradeoffs**

One tradeoff my scheduler makes is that its conflict detection only checks for exact matches on the same due date and start time. For example, it will warn me if two tasks are both scheduled at 18:00 on the same day, but it will not detect a partial overlap such as one task running from 18:00 to 18:20 and another starting at 18:10. I considered a more advanced overlap-based algorithm, but I chose the exact-match approach because it is simpler to implement, easier to read, and good enough for a lightweight class project where the main goal is to show useful scheduling logic without making the system too complex too early.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI, especially VS Code Copilot, as a design and implementation partner rather than as an autopilot tool. Copilot was most helpful when I was breaking the project into phases: drafting class ideas, suggesting method signatures, helping write and explain test cases, and proposing small algorithm improvements for sorting, filtering, recurrence, and conflict detection. I also used it to help think through how the Streamlit UI should reflect the smarter backend instead of staying disconnected from the scheduling logic.

The most effective Copilot features for this project were Chat for brainstorming and targeted questions, inline suggestions for small refactors, and test-generation support when I was building out `tests/test_pawpal.py`. The most helpful prompts were specific and scoped, such as asking how to sort `"HH:MM"` values with `sorted()` and a lambda, how to use `timedelta` to roll a daily task forward by one day, or what the most important edge cases were for a scheduler with recurring tasks and conflict warnings.

**b. Judgment and verification**

One moment where I did not accept the AI suggestion as-is was when thinking about conflict detection and algorithm simplification. A more compact, more "Pythonic" version could have used a dictionary grouping strategy or a more advanced overlap-based approach. I chose not to jump to that version because even if it was shorter, it would have been harder to explain and maintain for this project. I kept the simpler exact-time conflict detection because it matched the assignment scope and made the scheduler's behavior easier to understand.

I evaluated AI suggestions by checking whether they matched my design goals, whether they kept responsibilities clean between `Task`, `Pet`, `Owner`, and `Scheduler`, and whether I could verify the behavior with tests. I did not treat AI output as automatically correct. For example, after making changes, I reran `pytest`, checked the CLI demo output, and in one case adjusted type annotations to stay compatible with Python 3.9. That process reminded me that AI can generate good ideas quickly, but the human still needs to decide if the suggestion is appropriate for the actual codebase.

---

## 4. Testing and Verification

**a. What you tested**

I tested the behaviors that mattered most to the scheduler's core logic. These included marking a task complete, adding a task to a pet, sorting tasks in chronological order, creating the next occurrence for daily and weekly recurring tasks, making sure non-recurring tasks do not clone themselves, and detecting same-time conflicts between tasks. I also ran the CLI demo to confirm that the output matched the intended scheduling behavior.

These tests were important because they covered the intelligent parts of the system rather than only the basic class structure. Without them, it would have been easy for sorting, recurrence, or conflict warnings to break silently while the app still looked like it was working. The tests gave me confidence that the scheduling rules were doing what I expected and that later refinements did not accidentally regress earlier features.

**b. Confidence**

I am reasonably confident that the scheduler works correctly for the main scenarios I implemented. Based on the automated tests and the CLI verification, I would rate my confidence as 4 out of 5 stars. The core behaviors are stable in the cases I tested, and the UI now reflects the main backend features instead of hiding them.

If I had more time, I would test more edge cases around the UI and around scheduling logic. For example, I would add tests for invalid time input, an owner with no pets, a pet with no tasks, filtering for a pet name that does not exist, trying to complete a task that is already complete, and more realistic time conflicts involving overlapping durations rather than exact time matches only.

---

## 5. Reflection

**a. What went well**

The part I am most satisfied with is how the project evolved from a simple task list into a smarter scheduler with clear layers of responsibility. The final system has a cleaner separation between the backend logic in `pawpal_system.py`, the automated tests, and the Streamlit interface. I am also proud that the app does not just store tasks anymore; it now sorts them, filters them, rolls recurring tasks forward, and warns about conflicts in a way that feels much closer to a real planning tool.

**b. What you would improve**

If I had another iteration, I would improve both the scheduling model and the UI. On the backend, I would redesign conflicts to consider overlapping task durations, not only exact-time matches. I would also consider introducing a more explicit scheduled task or occurrence object so recurring tasks and calendar-style planning could be modeled more cleanly. On the frontend, I would add controls for marking tasks complete directly in Streamlit and make the filtering and schedule-generation flow more interactive.

**c. Key takeaway**

My biggest takeaway is that working with powerful AI tools still requires a clear human architect. Copilot helped me move faster, generate ideas, and reduce blank-page friction, but it worked best when I gave it focused prompts and used separate chat sessions for different phases of the project. Splitting design, algorithm work, testing, and documentation into separate conversations helped me stay organized and made it easier to judge AI suggestions in the right context.

I learned that being the "lead architect" means keeping the system coherent even when the AI offers many possible directions. My role was to decide what belonged in each class, which algorithms were appropriate for the assignment, which suggestions were too complex, and how to verify that the final behavior actually matched my goals. AI made me faster, but the quality of the result still depended on my judgment, structure, and willingness to verify every important change.
