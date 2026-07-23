# Test Automation Process, Lifecycle & Framework Types — Hands-On 3

## Task 1: Automation Decision and Test Case Selection

### 17. Five Criteria for Deciding What to Automate

**Scenario used for all 5 criteria below:** "Test that POST /api/courses/ returns 201 with the correct course data when valid input is provided."

1. **Is it repetitive?** — Will this exact test be run again and again (every build, every release)? For our scenario: yes, this test would run every time someone changes the courses API, so it's a strong candidate for automation.

2. **Is it stable?** — Does the feature being tested change often, or is it settled? Creating a course with valid input is a core, stable behavior that isn't likely to change every sprint, so it's safe to automate.

3. **Is the expected result predictable and easy to check?** — Can we clearly say "if input X, then output should be Y" without needing human judgement? Here, yes — valid input should always give status 201 and the correct data back, which is easy to assert automatically.

4. **How high is the risk if this breaks?** — Course creation is a core feature of the whole app; if this endpoint breaks, the entire system is unusable. High-risk features are worth automating so we catch breaks immediately.

5. **How much manual effort does it save over time?** — Running this exact check manually every time a developer changes code would be slow and repetitive. Automating it once means it can run in seconds, every single time, with no extra manual effort.

Since this test case is repetitive, stable, predictable, high-risk if broken, and saves a lot of manual effort — it's a clear candidate for automation.

---

### 18. Automate or Manual — Course Management API Test Cases

| # | Test Case | Decision | Reason |
|---|---|---|---|
| a | Regression test for all CRUD endpoints after every code change | **Automate** | This runs repeatedly after every change — exactly the kind of repetitive, predictable test automation is built for |
| b | Exploratory testing of a new search feature | **Manual** | Exploratory testing means a human is creatively poking around to find unexpected issues — there's no fixed script to automate here |
| c | Performance test: 100 concurrent users calling GET /api/courses/ | **Automate** | It's impossible for a human to manually send 100 simultaneous requests — this needs a tool to simulate the load |
| d | UI test for the login form | **Automate** | Login is used constantly and rarely changes in behavior, so it's worth automating with a Selenium test, run on every build |
| e | Verify the API documentation (Swagger) is accurate | **Manual** | Checking if written descriptions "make sense" and match reality needs human judgement, not something a script can easily verify |
| f | Smoke test: verify the API is reachable after deployment | **Automate** | This is a simple, repeatable check (is the server up?) that should run automatically after every single deployment |

---

### 19. Test Automation ROI

**What is Automation ROI?**
ROI (Return on Investment) for automation means comparing the time/effort spent building an automated test against the time/effort it saves over many runs, compared to running that same test manually every time.

**Given numbers:**
- Time to automate the test (one-time setup): 4 hours = 240 minutes
- Time to run the same test manually, each time: 30 minutes

**Step 1: Basic breakeven point (before maintenance is considered)**

Every time the automated test runs, we save roughly 30 minutes compared to doing it manually (assuming the automated run itself takes almost no time).

```
Breakeven runs = Automation setup time / Manual run time
Breakeven runs = 240 minutes / 30 minutes
Breakeven runs = 8 runs
```

So after just **8 runs**, the automated test has already saved as much time as it took to build it.

**Step 2: Accounting for 20% maintenance overhead after the 10th run**

After the 10th run, let's assume each further run needs a bit of maintenance work (fixing broken locators, updating test data, etc.) equal to 20% of the manual run time:

```
Maintenance overhead per run (after run 10) = 20% of 30 minutes = 6 minutes
Net time saved per run after run 10 = 30 minutes - 6 minutes = 24 minutes
```

**Conclusion:** Since the automation already pays for itself by run 8 (before the extra maintenance cost even kicks in at run 10), it's still a solid investment overall. From run 11 onward, we're saving a bit less per run (24 minutes instead of 30), but we're still saving time on every single run, not losing money on the investment.

---

### 20. Flaky Tests

**What is a flaky test?**
A flaky test is a test that sometimes passes and sometimes fails, even though nothing actually changed in the code being tested. It's unreliable — you can't trust its result.

**Example:**
A Selenium test clicks "Submit" on the course creation form and immediately checks if a success message appeared. Sometimes it passes, sometimes it fails — not because the feature is broken, but because the test checked for the message before the page had time to actually show it.

**3 Strategies to Prevent or Fix Flaky Tests:**

1. **Replace time.sleep() with explicit waits.** Instead of guessing a fixed delay, use `WebDriverWait` with `expected_conditions` to wait for the actual element/condition to be ready before checking it.

2. **Use unique, stable locators.** Avoid locators tied to page position (like absolute XPath) which can silently point to the wrong element if the page layout shifts slightly. Prefer IDs or unique attributes.

3. **Isolate test data between runs.** If tests share the same database records (e.g. always using a course named "Test Course"), one test's leftover data can cause the next test run to unexpectedly fail. Create fresh, unique test data for each run instead of reusing the same fixed values.

---

## Task 2: Compare Automation Framework Types

### 21. Comparison of the 5 Framework Types

**Linear Framework**
Description: Tests are written as simple, straight-line scripts — record and playback style, one step after another, with no reusable functions.
Advantage: Very quick and easy to write for beginners, no setup needed.
Disadvantage: Any small UI change (like a button ID changing) breaks every script that used it, since nothing is shared or reused.
Example use: A one-time quick check that the Course Management login page loads correctly, that we don't plan to maintain long-term.

**Modular Framework**
Description: Common actions (like "login", "create course") are broken into small reusable functions, and test scripts call these functions instead of repeating the same steps.
Advantage: If the login steps change, you only need to update one function, not every test that uses login.
Disadvantage: Takes more upfront planning and coding skill compared to Linear.
Example use: Writing a reusable `create_course()` function that many different test cases in the Course Management suite can call.

**Data-Driven Framework**
Description: The test logic (steps) stays the same, but it runs multiple times with different sets of input data pulled from an external file (like a CSV or Excel sheet).
Advantage: Easily test many different input combinations without writing a new test for each one.
Disadvantage: If the test steps themselves change, you have to redesign the framework structure, not just the data.
Example use: Testing course creation with 20 different combinations of course names, some valid and some invalid, all using the same test logic.

**Keyword-Driven Framework**
Description: Test steps are written as plain keywords (like "Click", "EnterText", "Verify") in a spreadsheet or table, and the framework translates these keywords into actual code behind the scenes.
Advantage: Non-technical team members can write and understand tests without knowing how to code.
Disadvantage: Takes significant time and effort to build the underlying keyword engine before any tests can even be written.
Example use: Letting a QA team member with no coding background write a test for the course search feature just by listing keywords and values in a spreadsheet.

**Hybrid Framework**
Description: Combines ideas from the other frameworks — usually Modular (reusable functions) plus Data-Driven (external test data), sometimes with Keyword-Driven elements too.
Advantage: Gets the strengths of multiple approaches — reusable, scalable, and flexible for different data sets.
Disadvantage: More complex to design and set up initially compared to any single framework type alone.
Example use: The full Selenium suite for the Course Management frontend — reusable login/course-creation functions, combined with data files for different test scenarios.

---

### 22. Recommended Framework for the Course Management Frontend Suite

**Requirements given:**
- Test login with 50 different user/password combinations
- Reuse login steps across 20 test cases
- Support both technical and non-technical team members writing tests

**Recommendation: Hybrid Framework** (combining Modular + Data-Driven, with some Keyword-Driven elements)

**Why:**
- The need to reuse login steps across 20 test cases points directly to **Modular** — build one `login()` function once, call it everywhere.
- The need to test 50 different user/password combinations points directly to **Data-Driven** — keep the login test logic the same, just loop through 50 rows of data from a file.
- The need for non-technical team members to write tests points to adding some **Keyword-Driven** elements — letting them describe test steps in a simple table/spreadsheet, which the framework translates into actual Selenium actions.

Combining all three into one Hybrid setup covers every requirement, instead of picking just one framework type and leaving a gap.

---

### 23. Hybrid Framework Folder Structure

```
CourseManagement_TestSuite/
│
├── config/
│   └── config.yaml              # base URL, browser type, timeouts, environment settings
│
├── test_data/
│   ├── login_credentials.csv    # 50 username/password combinations for data-driven login tests
│   └── course_data.csv          # sample course names/details for course creation tests
│
├── page_objects/
│   ├── login_page.py            # all locators and actions for the login page
│   └── course_page.py           # all locators and actions for the course creation page
│
├── utils/
│   ├── driver_setup.py          # reusable function to start/stop the Selenium driver
│   └── data_reader.py           # reusable function to read test data from CSV files
│
├── keywords/
│   └── keyword_engine.py        # translates plain keywords (Click, EnterText, Verify) into Selenium actions
│
├── tests/
│   ├── test_login.py            # test cases that use login_page.py + login_credentials.csv
│   └── test_course_creation.py  # test cases that use course_page.py + course_data.csv
│
└── requirements.txt              # selenium, pytest, webdriver-manager, etc.
```

**Quick explanation of each folder:**
- `config/` — settings that shouldn't be hardcoded inside test files (URLs, timeouts)
- `test_data/` — the actual input values used for data-driven tests
- `page_objects/` — one file per page, holding that page's locators and actions (reused everywhere)
- `utils/` — small reusable helper functions not tied to any one page
- `keywords/` — the translation layer that lets non-technical testers write plain-word test steps
- `tests/` — the actual test files that call everything above together