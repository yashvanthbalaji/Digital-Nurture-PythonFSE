# SDLC vs TDLC — V-Model & Agile QA Integration — Hands-On 2

## Task 1: V-Model Mapping

### 9. The V-Model Diagram

The V-Model shows development phases on the left going down, and testing phases on the right going up, with Coding sitting at the very bottom connecting both sides.

```
Requirements              Acceptance Testing
      \                          /
       System Design      System Testing
             \                  /
        Architecture     Integration Testing
        Design                 /
               \              /
           Module Design   Unit Testing
                    \        /
                     \      /
                      Coding
```

Each phase on the left has a matching phase on the right — they're connected, not separate. Whatever gets decided during a development phase directly shapes how the matching testing phase will be done.

---

### 10. Test Artifacts Produced at Each Phase

| SDLC Phase | Matching TDLC Phase | Test Artifact Produced |
|---|---|---|
| Requirements | Acceptance Testing | Acceptance Test Plan is written during this phase, based on what the business/user actually wants |
| System Design | System Testing | System Test Plan is written, based on how the whole system is expected to behave end-to-end |
| Architecture Design | Integration Testing | Integration Test Plan is written, based on how different modules/components are expected to talk to each other |
| Module Design | Unit Testing | Unit Test Cases are written, based on the exact logic planned for each individual function/module |

The important idea here: test planning starts way before any code is written. We don't wait for coding to finish to start thinking about tests.

---

### 11. Entry and Exit Criteria for Each Testing Level

**Unit Testing**
- Entry Criteria: Code for the module/function is complete and compiles without errors. Unit test cases are written and reviewed.
- Exit Criteria: All planned unit test cases have been executed. All critical bugs found are fixed. Code coverage meets the agreed target (e.g. 80%).

**Integration Testing**
- Entry Criteria: Unit testing is complete and passed. Individual modules are ready to be connected together. Integration test cases are ready.
- Exit Criteria: All integration test cases executed. Data flows correctly between connected modules/APIs. No critical/high defects remain open.

**System Testing**
- Entry Criteria: All modules are integrated into one complete system. Integration testing is complete and passed. Test environment is set up and stable.
- Exit Criteria: All system test cases executed covering full end-to-end flows. System meets the functional requirements. No critical/high severity defects remain open.

**User Acceptance Testing (UAT)**
- Entry Criteria: System testing is complete and passed. The application is deployed to a UAT/staging environment that mirrors production. Business/end users are available to test.
- Exit Criteria: All acceptance criteria for the user stories are met. The business/admin user has approved and signed off that the system does what they need.

---

### 12. Two Places QA Should Engage Early in the Course Management API Project

QA shouldn't only show up once code is done. Two good early points to get involved:

1. **During the Requirements phase** — QA should review the requirements document for the Course Management API before any code is written. For example, checking: "What exactly happens if someone tries to create a course with a name that already exists?" If this isn't clearly answered in the requirements, it's much cheaper to clarify it now than to discover the confusion after the feature is built.

2. **During Architecture/API Design** — QA should review the planned API contract (endpoints, request/response formats, status codes) for the Course Management API before development starts coding it. For example, confirming the team has agreed what status code `POST /api/courses/` should return for a duplicate course (409? 400?) — catching this early avoids inconsistent behavior being built into the code and needing rework later.

---

## Task 2: Agile QA and Shift-Left Testing

### 13. Three Problems Waterfall Testing Causes for the Course Management API

1. **Bugs are found very late.** If testing only starts after the entire Course Management API is fully built, a basic issue like "duplicate course names aren't handled properly" might only get discovered weeks after that code was written — making it slower and more expensive to fix, since the developer has already moved on to other work.

2. **Requirements misunderstandings aren't caught early.** If QA only gets involved at the end, nobody checks earlier whether the requirements for course creation were even clear or testable. By the time testing starts, it might be too late to easily change the design if something was misunderstood from the start.

3. **Less time to actually fix what's found.** Since all testing is squeezed into one phase at the very end, when many bugs are discovered close to the deadline, there's very little time left to properly fix and retest everything — leading to rushed fixes or bugs shipped to production.

---

### 14. QA's Role in Each Agile Ceremony

**Sprint Planning**
QA helps define the Acceptance Criteria for each user story before development starts — clarifying exactly what "done" looks like for a feature, so both developers and testers agree on the expected behavior upfront.

**Daily Standup**
QA shares any blocking issues — for example, if a test environment is down, or if a bug found yesterday is blocking further testing of a feature, this gets raised so the team can act on it quickly.

**Sprint Review**
QA helps demo the tested features to stakeholders, showing that what was built actually works as expected, based on the testing done during the sprint.

**Retrospective**
QA gives feedback on what testing-related process issues came up during the sprint — for example, "we kept finding bugs that could have been caught if we reviewed requirements together earlier" — and suggests process improvements for the next sprint.

---

### 15. Four Shift-Left Practices Applied to the Course Management API

**(a) Reviewing requirements for testability**
Before development starts, QA reads through the requirement "Admin can create a course" and asks questions like: what fields are required? What happens with duplicate names? What's the max length for a course name? This catches gaps before coding even begins.

**(b) Writing test cases before code (TDD/BDD)**
Before writing the actual `POST /api/courses/` endpoint code, the team first writes a test like "creating a course with valid data should return 201 Created" — then writes just enough code to make that test pass. This forces clear thinking about expected behavior before implementation.

**(c) Static code analysis**
Running an automated tool (like a linter or code quality scanner) on the Course Management API codebase to catch things like unused variables, bad practices, or potential bugs — without even running the actual application. This happens as code is written, not after.

**(d) API contract testing before integration**
Before the frontend team builds the course-creation form, they agree with the backend team on the exact API contract (what fields `POST /api/courses/` expects, what response format it returns) and test against that contract early — instead of waiting until both sides are fully built to discover mismatches.

---

### 16. Acceptance Criteria in Given-When-Then Format

**User Story:** As a college admin, I want to create a new course, so that students can enroll in it.

**Scenario 1: Happy Path**
```gherkin
Given I am logged in as a college admin
When I submit a new course with a valid course name and all required details
Then the course should be created successfully
And I should see a confirmation message
And the new course should appear in the course list
```

**Scenario 2: Duplicate Course Code**
```gherkin
Given I am logged in as a college admin
And a course with the code "CS101" already exists
When I try to create a new course using the same code "CS101"
Then the system should reject the request
And I should see an error message saying the course code already exists
And no duplicate course should be created in the database
```

**Scenario 3: Missing Required Fields**
```gherkin
Given I am logged in as a college admin
When I try to create a new course without entering a course name
Then the system should reject the request
And I should see an error message indicating the course name is required
And no course should be created in the database
```
<p align="center">
  <strong>All the works, solutions, code, and documentation in this repository were completed by</strong><br>
  <strong>BALAJI A</strong><br>
  <strong>Email: 333yashvanthbalaji@gmail.com</strong><br>
  <strong>Superset ID: 7995004</strong>
</p>