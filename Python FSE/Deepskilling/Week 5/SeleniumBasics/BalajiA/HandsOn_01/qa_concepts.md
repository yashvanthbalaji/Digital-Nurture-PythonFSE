# QA Concepts & Functional Testing — Hands-On 1

## Task 1: Mapping Testing Types to the Course Management API

### 1. Test Cases for Each Testing Level

**Unit Testing**
Testing one small function by itself, with nothing else involved.
- Example: Test the function that checks if a course name is empty before saving it to the database. We just call this one function directly with an empty string and check it returns `False` (invalid).

**Integration Testing**
Testing two parts of the system working together.
- Example: Test that when we call the `POST /api/courses/` endpoint, it actually talks to the database correctly and a new row gets created in the `courses` table. We're not just checking the API responds — we're checking the API and database work together properly.

**System Testing**
Testing the whole flow from start to finish, like a real request going through the entire app.
- Example: Send a full `POST /api/courses/` request with course details, then immediately send a `GET /api/courses/{id}` request to fetch it back, and confirm the data returned matches exactly what we sent. This checks the complete request → database → response cycle.

**User Acceptance Testing (UAT)**
Testing from the point of view of a real person who will actually use the system, not a developer.
- Example: A college admin logs into the system, adds a new course called "Data Structures", and checks it shows up correctly in the course list on the dashboard — without needing to know anything about APIs or databases.

---

### 2. Functional vs Non-Functional Classification

All 4 test cases above are **Functional** tests — they check "does the feature actually work?"

**Non-Functional example (something different):**
- Test: Send 100 `POST /api/courses/` requests at the same time and check the API still responds within 2 seconds each, without crashing.
- This is a **Performance** test. It's non-functional because we're not checking *if* the feature works, we're checking *how well* it works under load.

---

### 3. Black-Box vs White-Box Testing

**Black-Box Testing**
You test the app from the outside, like a normal user or tester would. You don't look at the code — you only care about input in, output out. Example: sending a request to `POST /api/courses/` and checking the response, without knowing how the code is written internally.

**White-Box Testing**
You test with full knowledge of the internal code. You can see the actual logic, loops, conditions, and write tests that target specific lines of code.

**Who does what:**
- QA testers usually do **Black-Box testing** — they focus on behavior and outcomes, not code.
- Developers usually do **White-Box testing** — they write unit tests while looking directly at their own code logic.

---

### 4. Formal Test Cases for POST /api/courses/

| Test Case ID | Description | Preconditions | Test Steps | Expected Result | Actual Result | Pass/Fail |
|---|---|---|---|---|---|---|
| TC_001 | Create a course with valid data | API server is running, database is connected | 1. Send POST request to /api/courses/ with valid course name and details 2. Check the response | Response returns status 201 Created, and the new course appears in the database | | |
| TC_002 | Create a course with an empty course name | API server is running | 1. Send POST request to /api/courses/ with course name left blank 2. Check the response | Response returns status 400 Bad Request with a proper error message, no course is created | | |
| TC_003 | Create a course with a duplicate course name | A course named "Data Structures" already exists in the database | 1. Send POST request to /api/courses/ with the same course name "Data Structures" 2. Check the response | Response returns status 409 Conflict (or similar), duplicate course is not created | | |

---

## Task 2: Defect Lifecycle & Severity Classification

### 5. Defect Lifecycle States

Here's how a bug moves through its life, from being found to being closed:

1. **New** — Tester finds a bug and logs it for the first time.
2. **Assigned** — A lead or manager assigns the bug to a specific developer.
3. **Open** — The developer starts looking into it, confirms it's a real bug.
4. **Fixed** — The developer has made the code change to fix it.
5. **Retest** — The tester checks the fix on a new build to confirm it's actually solved.
6. **Verified** — Tester confirms the bug no longer happens, fix is working.
7. **Closed** — Bug is officially done, nothing more to do.

**Two other paths that can happen instead:**

- **Rejected** — The developer or lead looks at the bug and decides it's not actually a bug (maybe it's working as intended, or the tester misunderstood the feature). Bug gets closed without any code change.
- **Deferred** — The bug is real, but the team decides to fix it later, not right now (maybe low priority, or no time before release). It gets postponed to a future release/sprint.

---

### 6. Severity and Priority for Each Bug

**a) POST /api/courses/ returns 500 Internal Server Error for all requests**
- Severity: **Critical**
- Priority: **P1**
- Why: The entire course creation feature is completely broken for every single user. Nothing works at all, so this needs to be fixed immediately.

**b) Course names longer than 150 characters are silently truncated without an error**
- Severity: **Medium**
- Priority: **P3**
- Why: The app doesn't crash and mostly works, but it's quietly losing user data without telling them, which is a real problem — just not urgent enough to stop everything for.

**c) The /docs Swagger page has a typo in the API description**
- Severity: **Low**
- Priority: **P4**
- Why: This doesn't affect how the app works at all. It just looks unprofessional. Can be fixed whenever, no rush.

**d) Login with correct credentials occasionally returns 401 on the first attempt (intermittent)**
- Severity: **Medium**
- Priority: **P1**
- Why: It doesn't happen every time, so on paper it looks less severe. But random login failures are extremely frustrating for users and usually mean something deeper and unstable is going on in the system — so this needs urgent attention even though it's "only sometimes."

---

### 7. Defect Report for Bug (a)

| Field | Details |
|---|---|
| Defect ID | DEF_001 |
| Title | POST /api/courses/ returns 500 Internal Server Error for all requests |
| Environment | Staging server, Chrome browser, Postman for API testing |
| Build Version | v1.2.0 |
| Severity | Critical |
| Priority | P1 |
| Steps to Reproduce | 1. Open Postman 2. Send a POST request to /api/courses/ with valid course data in the body 3. Observe the response |
| Expected Result | API should return status 201 Created, and the new course should be saved in the database |
| Actual Result | API returns status 500 Internal Server Error, no course gets created |
| Attachments | screenshot of 500 error |

---

### 8. Severity vs Priority — What's the Difference

**Severity** = how badly this bug breaks the system/functionality.
**Priority** = how quickly this bug needs to be fixed, business-wise.

They usually go together, but not always. Here's a real example:

Imagine there's a typo on the company CEO's personal dashboard — it says "Wlecome back" instead of "Welcome back". This is a spelling mistake, nothing is broken, the app works perfectly fine. So **Severity is Low**. But because the CEO sees this every single day and it looks embarrassing, the team decides to fix it right away before anything else. So **Priority is High**.

That's the whole point — Severity is about technical impact, Priority is about business/urgency. A bug can be small and unimportant technically, but still jump to the front of the line because of who sees it or when it matters.