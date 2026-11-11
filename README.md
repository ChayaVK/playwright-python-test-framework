# Playwright UI Test Framework (Python)

A ready-to-use test automation framework built with **Playwright + Python + pytest**.
It comes with its own small demo web app (the **Practice Shop**) and a REST API, written in plain Python, so every test runs on your machine with no outside website and no internet connection needed once it is installed.

Use it as it is to learn, or rename it and point it at your own application.

> Tested: 47 tests in Chromium on a local machine, one by one and in parallel (`pytest -n auto`).

---

## Contents

1. [What is inside](#1-what-is-inside)
2. [Before you start](#2-before-you-start)
3. [Set up the project](#3-set-up-the-project)
4. [Run the tests in VS Code](#4-run-the-tests-in-vs-code)
5. [Run from the command line](#5-run-from-the-command-line)
6. [Project structure](#6-project-structure)
7. [How the framework works](#7-how-the-framework-works)
8. [Configuration and environments](#8-configuration-and-environments)
9. [Reports, traces, screenshots and videos](#9-reports-traces-screenshots-and-videos)
10. [Add a new page and a new test](#10-add-a-new-page-and-a-new-test)
11. [Data-driven tests: JSON and CSV](#11-data-driven-tests-json-and-csv)
12. [API tests and UI + API tests](#12-api-tests-and-ui--api-tests)
13. [Parallel, cross-browser and mobile runs](#13-parallel-cross-browser-and-mobile-runs)
14. [Run in Docker](#14-run-in-docker)
15. [Run in GitHub Actions](#15-run-in-github-actions)
16. [Make it your own framework](#16-make-it-your-own-framework)
17. [Troubleshooting](#17-troubleshooting)
18. [Explain this framework in an interview](#18-explain-this-framework-in-an-interview)

## 1. What is inside

| Area | What is included |
| --- | --- |
| Design | Page Object Model, a reusable Header component, BasePage |
| Fixtures | pytest fixtures that hand page objects and API clients to tests |
| Login | Logs in once per run and reuses the saved session (storage state) |
| Data-driven | `@pytest.mark.parametrize` with JSON and CSV test data |
| API | ApiClient + UsersApi with token auth and full CRUD tests |
| UI + API | Compare the UI with the API, seed state, mock network calls |
| Browsers | Chromium, Firefox, WebKit and mobile devices (for example Pixel 7) |
| Environments | `env/.env.local`, `.env.qa`, `.env.staging`, picked by `TEST_ENV` |
| Utilities | Price parsing and sums, random test data, JSON and CSV readers, step logger |
| Reports | HTML report (with a screenshot of each failure), JUnit XML, traces, screenshots and videos |
| Speed | Parallel runs with pytest-xdist, reruns of failed tests with pytest-rerunfailures |
| CI/CD | GitHub Actions (one job per browser) and a Docker workflow |
| Docker | Dockerfile on the official Playwright Python image + docker-compose |

Test suites at a glance:

| Folder | Tests | What they cover |
| --- | --- | --- |
| `tests/ui` | 25 | Login, products, sorting, cart, checkout, alerts, frames, tabs, waits, dropdown, checkbox, upload, web table |
| `tests/data_driven` | 11 | Login errors from JSON, checkout form errors from CSV, order totals from JSON |
| `tests/e2e` | 4 | UI vs API prices, seeding the cart, network mocking, screenshot evidence |
| `tests/api` | 7 | Health, products, login, users CRUD with a token |

## 2. Before you start

1. Install **Python 3.10 or newer** from <https://www.python.org/downloads/>. On Windows, tick **Add python.exe to PATH** in the installer. Check it in a terminal with `python --version`.
2. Install **Git** from <https://git-scm.com>. Check it with `git --version`.
3. Install **VS Code** from <https://code.visualstudio.com> and add the extension **Python** (publisher: Microsoft).
4. For Docker runs only: install **Docker Desktop** from <https://www.docker.com/products/docker-desktop> and start it.

## 3. Set up the project

1. Get the code. Either clone it:

    ```bash
    git clone https://github.com/<username>/playwright-python-test-framework.git
    ```

    or unzip the project folder you downloaded.

2. In VS Code choose **File > Open Folder** and pick `playwright-python-test-framework`.
3. Open the terminal (**Terminal > New Terminal**) and create a virtual environment, so the packages stay inside this project:

    ```bash
    python -m venv .venv
    ```

4. Turn it on (you do this every time you open a new terminal):

    | Your system | Command |
    | --- | --- |
    | Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
    | Windows (Command Prompt) | `.venv\Scripts\activate.bat` |
    | macOS / Linux | `source .venv/bin/activate` |

    The prompt now starts with `(.venv)`. If PowerShell says running scripts is disabled, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once and try again.

5. Install the packages and the browsers:

    ```bash
    pip install -r requirements.txt
    python -m playwright install
    ```

    The first command installs pytest, Playwright and the plugins. The second downloads Chromium, Firefox and WebKit (a few hundred MB, one time only).

6. Run everything once:

    ```bash
    pytest
    ```

    You should see `47 passed`.

> You do not need to start the demo app yourself. The tests start the Practice Shop at <http://localhost:3000> before the first test and stop it at the end (see `pytest_sessionstart` in `tests/conftest.py`).

## 4. Run the tests in VS Code

1. Press **Ctrl+Shift+P**, type **Python: Select Interpreter** and pick the one in `.venv`.
2. Click the **Testing** icon (the flask) in the left bar. VS Code finds the tests through `.vscode/settings.json`.
3. Click the play button next to any test, file or folder to run it.
4. To watch the browser, run from the terminal with `pytest --headed` (see the next section).

## 5. Run from the command line

| What you want | Command |
| --- | --- |
| Whole suite (Chromium) | `pytest` |
| Faster, in parallel | `pytest -n auto` |
| Firefox / WebKit | `pytest --browser firefox` / `pytest --browser webkit` |
| All three browsers | `pytest --browser chromium --browser firefox --browser webkit` |
| Mobile (Pixel 7) | `pytest tests/ui/test_products.py --device "Pixel 7"` |
| Smoke tests only | `pytest -m smoke` |
| Regression tests only | `pytest -m regression` |
| Data-driven tests only | `pytest -m data` |
| API tests only | `pytest -m api` |
| Watch the browser | `pytest --headed --slowmo 500` |
| Rerun failed tests up to 2 times | `pytest --reruns 2` |
| Run only the tests that failed last time | `pytest --last-failed` |
| Step through with the Playwright Inspector | Windows PowerShell: `$env:PWDEBUG=1; pytest -s tests/ui/test_cart.py`<br>macOS / Linux: `PWDEBUG=1 pytest -s tests/ui/test_cart.py` |
| Record a new test by clicking | `python demo_app/server.py`, then in a second terminal `playwright codegen http://localhost:3000` |

### Run a single file or test

```bash
pytest tests/ui/test_cart.py
pytest tests/ui/test_cart.py::test_cart_is_kept_after_a_reload
pytest -k "sorting and price"
```

`-k` picks tests whose names contain the words, so `-k "sorting and price"` runs the two price sorting tests.

## 6. Project structure

```text
playwright-python-test-framework/
├── api/                    API clients: ApiClient (base URL, token) and UsersApi
├── components/             Parts shared by many pages: Header
├── config/settings.py      Reads env/.env.<TEST_ENV> into one Settings object
├── data/                   Test data: login_cases.json, checkout_cases.csv, products.json
├── demo_app/               The Practice Shop: HTML pages + server.py (web app and REST API)
├── env/                    .env.local, .env.qa, .env.staging
├── pages/                  Page objects: one class per page, all extend BasePage
├── test-files/             Files used by tests (the upload test)
├── tests/
│   ├── conftest.py         Fixtures: demo app, login once, page objects, API clients
│   ├── ui/                 UI tests
│   ├── data_driven/        Tests generated from JSON and CSV rows
│   ├── e2e/                UI and API together
│   └── api/                API tests
├── utils/                  price.py, random_data.py, data_reader.py, logger.py
├── .github/workflows/      tests.yml (every push) and docker.yml (nightly / on demand)
├── Dockerfile, docker-compose.yml
├── pytest.ini              Default options, markers, report settings
└── requirements.txt        Packages to install
```

## 7. How the framework works

**Page objects.** Each page is a class in `pages/` that holds its locators and actions. Tests call `products_page.add_to_cart("Laptop Bag")` instead of repeating selectors. When the page changes, you fix one class, not every test.

**Fixtures.** `tests/conftest.py` defines fixtures such as `products_page`, `cart_page` and `users_api`. A test lists them as parameters and pytest builds them:

```python
def test_cart_shows_exactly_the_added_items(products_page: ProductsPage, cart_page: CartPage):
```

pytest-playwright adds the built-in fixtures `page`, `context`, `browser` and `playwright`.

**Log in once.** The `auth_state` fixture logs in a single time per run and saves the session (local storage) to a file. The `browser_context_args` fixture hands that file to every new browser context, so UI tests start logged in. Tests that must start logged out use:

```python
pytestmark = pytest.mark.browser_context_args(storage_state=None)
```

**Base URL.** The `base_url` fixture returns `BASE_URL` from the settings, so tests write `page.goto("products.html")`.

**Web-first assertions.** `expect(locator).to_have_text(...)` waits and retries until the condition is true or the timeout ends. No `time.sleep()` anywhere.

**Test ids.** The app marks elements with `data-test="..."`, so the `test_id_attribute` fixture tells Playwright to use that attribute for `get_by_test_id()`.

## 8. Configuration and environments

Settings come from `env/.env.<TEST_ENV>`. `TEST_ENV` defaults to `local`.

| Setting | Meaning |
| --- | --- |
| `BASE_URL` | Address of the web app |
| `API_URL` | Address of the REST API |
| `APP_USERNAME`, `APP_PASSWORD` | Login used by the tests |
| `LOCKED_USERNAME` | A user the app blocks |
| `START_DEMO_APP` | `true` starts the Practice Shop before the tests |

Pick an environment:

| Your system | Command |
| --- | --- |
| Windows PowerShell | `$env:TEST_ENV="qa"; pytest` |
| macOS / Linux | `TEST_ENV=qa pytest` |

Values already set in the terminal or CI win over the file, so keep real passwords out of Git and set them as secrets.

## 9. Reports, traces, screenshots and videos

After every run:

| What | Where | How to open |
| --- | --- | --- |
| HTML report | `reports/report.html` | Double-click it. Failed tests include a screenshot. |
| JUnit XML (for CI tools) | `test-results/junit.xml` | Read by Jenkins, Azure DevOps, GitHub and others |
| Trace of each failed test | `test-results/<test name>/trace.zip` | `playwright show-trace test-results/<test name>/trace.zip` |
| Screenshot and video of each failed test | `test-results/<test name>/` | Open the `.png` and `.webm` files |

These come from `pytest.ini`: `--tracing retain-on-failure`, `--screenshot only-on-failure` and `--video retain-on-failure` keep the files only for tests that fail. Change them to `on` to keep them for every test.

## 10. Add a new page and a new test

1. Create `pages/my_page.py`:

    ```python
    from playwright.sync_api import Page

    from pages.base_page import BasePage


    class MyPage(BasePage):
        path = "my-page.html"

        def __init__(self, page: Page):
            super().__init__(page)
            self.save_button = page.get_by_role("button", name="Save")
    ```

2. Add a fixture to `tests/conftest.py`:

    ```python
    @pytest.fixture
    def my_page(page: Page) -> MyPage:
        return MyPage(page)
    ```

3. Write a test in `tests/ui/test_my_page.py`. The file name and the function name must start with `test_`:

    ```python
    import pytest
    from playwright.sync_api import expect


    @pytest.mark.smoke
    def test_save_button_is_visible(my_page):
        my_page.open()
        expect(my_page.save_button).to_be_visible()
    ```

## 11. Data-driven tests: JSON and CSV

`@pytest.mark.parametrize` turns one test function into one test per data row. `ids` gives each test a readable name in the report:

```python
CASES = read_json("login_cases.json")

@pytest.mark.parametrize("case", CASES, ids=[c["case"] for c in CASES])
def test_login_shows_an_error(login_page, case):
```

Add a row to `data/login_cases.json` and you get a new test. `data/checkout_cases.csv` works the same way through `read_csv()`, which uses Python's built-in `csv` module.

## 12. API tests and UI + API tests

`ApiClient` wraps Playwright's `APIRequestContext`: it adds the base URL and, after `login()`, the token. `UsersApi` keeps the `/users` paths in one place. The `users_api` fixture hands tests a client that is already logged in:

```python
def test_create_read_update_and_delete_a_user(users_api):
    created = users_api.create({"name": "New Tester", "email": random_email("tester")})
    assert created.status == 201
```

`tests/e2e/test_ui_and_api.py` shows how to compare UI prices with the API, seed the cart through local storage, mock a response with `page.route()`, and save a screenshot as evidence.

## 13. Parallel, cross-browser and mobile runs

- `pytest -n auto` runs tests in parallel, one worker per CPU core (pytest-xdist). Every test gets its own browser context, so tests do not share state.
- `--browser firefox` or `--browser webkit` picks the browser. Repeat the option to run several.
- `--device "Pixel 7"` emulates a phone: screen size, touch and user agent.
- Skip a test in one browser with `@pytest.mark.skip_browser("webkit")`, or run it only in one with `@pytest.mark.only_browser("chromium")`.

## 14. Run in Docker

```bash
docker build -t pw-python-tests .
docker run --rm --ipc=host pw-python-tests
```

Or, with reports copied back to your machine:

```bash
docker compose up --build --abort-on-container-exit
```

The image is `mcr.microsoft.com/playwright/python`, which already contains the browsers. Keep its version the same as `playwright` in `requirements.txt`.

## 15. Run in GitHub Actions

Push the project to GitHub and `.github/workflows/tests.yml` runs on every push and pull request to `main`: one job per browser (Chromium, Firefox, WebKit), in parallel, with one rerun for failed tests. Download the reports from the run's **Artifacts** section. Use **Actions > Playwright Python Tests > Run workflow** to run only one marker, for example `smoke`.

`.github/workflows/docker.yml` builds the Docker image and runs the suite inside it every weekday night, or whenever you start it by hand.

## 16. Make it your own framework

1. Point `env/.env.qa` at your app and set `START_DEMO_APP=false`.
2. Replace the page objects in `pages/` with your app's pages, and the tests in `tests/` with your own.
3. Change `data/` to your test data, and `api/` to your API's resources.
4. Delete `demo_app/` when you no longer need it.
5. Store real logins as CI secrets (`APP_USERNAME`, `APP_PASSWORD`), never in Git.

## 17. Troubleshooting

| Problem | Fix |
| --- | --- |
| `python` is not recognized | Reinstall Python and tick **Add python.exe to PATH**, or use `py` on Windows |
| `ModuleNotFoundError: No module named 'playwright'` | The virtual environment is not on. Run the activate command from step 3.4 |
| `Executable doesn't exist ... run playwright install` | Run `python -m playwright install` |
| `The Practice Shop did not start` | Port 3000 is in use. Close the other program, or set `DEMO_PORT` and the URLs in `env/.env.local` to another port |
| A test passes alone but fails with `-n auto` | It depends on another test. Make each test create its own data |
| VS Code shows no tests | Select the `.venv` interpreter (section 4) and click **Refresh Tests** |

## 18. Explain this framework in an interview

> "It's a Playwright framework in Python with pytest. Pages are page objects that extend a BasePage, and a Header component is shared by all pages. pytest fixtures in conftest.py build the page objects and API clients, so tests only list what they need. We log in once per run and reuse the storage state, which saves time. Test data lives in JSON and CSV files, and parametrize creates one test per row. API tests use Playwright's request context through an ApiClient with token auth, and some tests combine API and UI, for example comparing prices or seeding data. Settings come from .env files per environment. We run in parallel with pytest-xdist, across Chromium, Firefox and WebKit, and keep traces, screenshots and videos for failures, plus an HTML report. GitHub Actions runs it on every push, and it also runs in Docker."
