import os
from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini
from agno.tools.file import FileTools
from dotenv import load_dotenv
load_dotenv()
# NOTE: Do NOT hardcode API keys. Agents should read them from environment variables.
GEMINI_KEY = os.getenv("GEMINI_API_KEY")  # Set in runner env if needed
print(GEMINI_KEY)
# Agent 1: Project Analyzer - analyzes project structure and requirements
project_analyzer = Agent(
    name="Project Analyzer",
    model=Gemini(id="gemini-2.5-pro", api_key=GEMINI_KEY),
    tools=[FileTools()],
    instructions=[
        # Primary goal
        "Analyze the repository root and determine the project's language, packaging system, and test layout.",
        # Discovery steps (explicit)
        "Detect presence of: requirements.txt, pyproject.toml, poetry.lock, Pipfile, setup.cfg, setup.py.",
        "Detect where tests live (common locations: tests/, test/, backend/tests/, src/*/tests).",
        "Identify the test runner command (prefer `python -m pytest -q`) and whether tests need package installation (e.g., imports from the package).",
        # CI recommendations
        "Recommend a single CI working-directory if project is a subpackage or monorepo; if multiple packages provide a matrix suggestion.",
        "Recommend the appropriate base Docker image (e.g., python:3.11-slim) and required build steps based on detected files.",
        # uv & pytest specifics
        "Prefer using `uv` for fast installs in CI; if `uv` not appropriate, provide exact pip commands.",
        "If tests require extras (e.g., [test] extras in pyproject.toml), note the exact install command: `uv pip install --system -e \"[test]\"` or `uv pip install --system -r requirements-dev.txt`.",
        # Safety and secrets
        "Do NOT output or write any secret values or hard-coded API keys into any file. Instead instruct usage of GitHub Actions secrets (e.g., `${{ secrets.GITHUB_TOKEN }}`, `${{ secrets.GHCR_PAT }}`) and repository variables.",
        # Output structure
        "Return a structured summary containing: detected package manager, test path(s), recommended test command, recommended install command(s), build image, and any special environment variables required at runtime."
    ]
)

# Agent 2: YAML Writer - creates the GitHub Actions workflow file
yaml_writer = Agent(
    name="YAML Writer",
    model=Gemini(id="gemini-2.0-flash", api_key=GEMINI_KEY),
    tools=[FileTools()],
    instructions=[
        # Create a robust CI workflow using uv
        "Create a GitHub Actions YAML workflow at `.github/workflows/ci-cd.yml` following the detected project structure provided by Project Analyzer.",
        # Workflow contents (explicit checklist)
        "Include steps: checkout, setup-python@v5, install uv via pip, install dependencies using `uv` with safe fallbacks, ensure pytest is installed using `uv`, run tests with `python -m pytest -q` targeting detected testpaths.",
        "If tests live in a subdirectory, set `working-directory` for install/test steps or pass the test path to pytest (e.g., `python -m pytest -q backend/tests`).",
        "Add caching hints for dependencies; recommend uv's cache behavior and optionally use `actions/cache` for pip wheel/cache if needed.",
        "Add a fail-safe debug step that prints `pwd`, `ls -la`, `python -V`, and `python -m pip list` when tests fail (use `if: failure()` or `if: always()` as appropriate).",
        "Add Docker build+push stage using `docker/build-push-action@v3` and `docker/login-action@v2` with `ghcr.io` and credentials from `${{ secrets.GITHUB_TOKEN }}` or a dedicated `${{ secrets.GHCR_PAT }}`. Do NOT write tokens into the file.",
        "Tag the image with `ghcr.io/${{ github.repository }}:${{ github.sha }}` and optionally `:latest` (also explain implications).",
        "Add optional artifact upload of test reports and coverage (junitxml and coverage.xml) using `actions/upload-artifact@v4` with `if: always()` so failures are available.",
        "Use `python -m pytest -q --junitxml=reports/junit.xml --cov=./ --cov-report=xml` if coverage is requested.",
        "Ensure `runs-on: ubuntu-latest` and that matrix support for python versions is present (default to 3.11), and include `needs: test` in deploy job.",
        # Safety & validation
        "Ensure the workflow references only GitHub Actions secrets for any credentials and never writes secrets to the repo.",
        # Write the file
        "Write the fully-formed YAML to `.github/workflows/ci-cd.yml` using FileTools.save or equivalent and return the path and a short summary."
    ]
)

# Agent 3: Validator - validates the YAML syntax and configuration
validator = Agent(
    name="YAML Validator",
    model=Gemini(id="gemini-2.5-pro", api_key=GEMINI_KEY),
    tools=[FileTools()],
    instructions=[
        # Read and validate YAML
        "Open `.github/workflows/ci-cd.yml` and validate YAML syntax and ontology for GitHub Actions.",
        "Check these specific items and auto-fix if possible:",
        " - uses: actions/setup-python@v5 (prefer v5) is present and placed before any python-related steps.",
        " - uv is installed (a step `pip install uv`) and `uv pip install --system ...` is used to install deps.",
        " - pytest is installed using uv and the run step uses `python -m pytest -q` (not bare `pytest`).",
        " - If tests are in a subfolder, ensure either `working-directory` is set or pytest is invoked with the correct path.",
        " - Docker login uses `docker/login-action@v2` and references secrets (no plaintext credentials).",
        " - Validate `docker/build-push-action@v3` uses `tags` with `${{ github.sha }}` and that `push: true` is present for deploy job.",
        " - If uploading artifacts (reports/coverage), ensure the paths exist or the steps create them before upload.",
        " - Confirm `if: always()` is used on artifact upload/debugging steps so files are available on failures.",
        " - Detect common pitfalls and fix: missing `pytest`, wrong working-directory, not installing package before tests (add `python -m pip install -e .` if detection shows tests import package), incorrect indentation, or invalid action names/versions.",
        # Don't write secrets
        "If the YAML contains any hard-coded tokens or looks like it will expose secrets, remove them and replace with secure `${{ secrets.* }}` placeholders and add a comment instructing the user to populate secrets in repository settings.",
        # Finally save
        "If corrections were applied, save the fixed file back to `.github/workflows/ci-cd.yml` and produce a short validation report describing fixes made and remaining recommendations."
    ]
)

# Optional Agent 4: Lint & Best-Practices (extra)
lint_agent = Agent(
    name="YAML Linter & Best Practices",
    model=Gemini(id="gemini-2.0-flash", api_key=GEMINI_KEY),
    tools=[FileTools()],
    instructions=[
        "Run a lightweight workflow lint against `.github/workflows/ci-cd.yml` and list any GitHub Actions deprecations or recommended upgrades.",
        "Recommend adding `concurrency` to prevent duplicate deployments on concurrent pushes: `concurrency: ${{ github.workflow }}-${{ github.ref }}`.",
        "Recommend pinning major versions of actions (e.g., `actions/checkout@v4`, `actions/setup-python@v5`) and explain why.",
        "Suggest minimizing permission scope for the GITHUB_TOKEN if possible, and provide the minimal permission snippet for the workflow (e.g., packages: write for publishing to GHCR).",
        "Return a short 'best practices' checklist to the user."
    ]
)

# Create the CI/CD setup team (includes validator & linter)
cicd_team = Team(
    name="CI/CD Setup Team",
    model=Gemini(id="gemini-2.5-pro", api_key=GEMINI_KEY),
    members=[project_analyzer, yaml_writer, validator, lint_agent],
    instructions=[
        "Run a sequential process: analyze repository -> generate workflow -> validate and lint -> output summary and actionable next steps.",
        "Produce a final short summary (markdown) that explains where to set secrets, what commands the CI will run, and how to run tests locally to reproduce CI failures.",
        "If any required files are missing (e.g., tests folder, pytest.ini) produce example files and add them to the repo (but do not place secrets)."
    ]
)

# Kick off the team to produce the workflow
# The `print_response` or execution method depends on your agno runtime; adjust if necessary.
cicd_team.print_response(
    "Create a GitHub Actions CI/CD pipeline that uses uv for installs, runs tests with pytest, and deploys a Docker image to ghcr.io. "
    "Ensure the workflow uses secrets for credentials, installs pytest, runs `python -m pytest -q` pointing at the detected tests folder, and includes a validation & lint step."
)
