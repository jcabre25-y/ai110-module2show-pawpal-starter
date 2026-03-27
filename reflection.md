# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

My initial design focused on three main actions the user should be able to perform in the app. First, the user should be able to add and manage pet and owner information so the system knows who the schedule is for and can consider basic preferences. Second, the user should be able to create and update pet care tasks such as feeding, walking, medication, grooming, and enrichment, including details like duration and priority. Third, the user should be able to generate and review a daily care schedule that selects tasks based on the available time and priorities, then clearly shows the order of tasks and the reasoning behind the plan.

To support those actions, I chose four main classes: `Owner`, `Pet`, `Task`, and `Scheduler`. The `Owner` class is responsible for storing information about the pet owner, including their name, available time, and general care preferences. The `Pet` class stores basic information about the animal, such as its name and species. The `Task` class represents an individual care activity and holds details like the task title, duration, and priority. The `Scheduler` class is responsible for the planning logic. It takes the owner, pet, and task information and uses it to organize tasks into a daily care schedule. I chose these classes because they separate the data from the scheduling behavior and make the system easier to understand and build.

**b. Design changes**

Yes, my design changed slightly after reviewing the class relationships. At first, I considered letting the `Owner` class store multiple pets, but the rest of the system was really being designed around planning for one pet at a time. That created a mismatch because the `Scheduler` only worked with a single `Pet`. Based on that feedback, I simplified the design by treating the current version of the app as a single-pet scheduling system. This makes the relationships clearer and keeps the logic easier to implement. I also recognized that if I expand the app later to support multiple pets, I may need to connect tasks more directly to a specific pet or redesign the scheduler to handle a list of pets instead of just one.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
