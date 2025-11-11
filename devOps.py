from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini
from agno.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.tools.file import FileTools
from train import codebaseKB

# Agent 1: Project Analyzer - analyzes project from RAG database
project_analyzer = Agent(
    name="Project Analyzer",
    model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
    knowledge=codebaseKB(),
    search_knowledge=True,
    tools=[FileTools()],
    instructions=[
        "You are an expert DevOps engineer specializing in CI/CD pipeline configuration.",
        "Search the codebase knowledge base to find and analyze key configuration files.",
        "Look for: pyproject.toml, requirements.txt, package.json, Dockerfile, setup.py, or similar files.",
        "Identify the programming language (Python, Node.js, etc.) and framework being used.",
        "Search for test files to determine the test framework (pytest, unittest, jest, etc.).",
        "Identify the package manager: uv for Python projects, npm/yarn for Node.js.",
        "Search for existing Dockerfile or determine the appropriate base image needed.",
        "Look for environment configuration files (.env.example, config files) to identify required variables.",
        "Analyze the project structure to understand the application entry point and build process.",
        "Provide a comprehensive summary including: language, framework, test commands, dependencies, Docker requirements, and environment setup based on the actual codebase."
    ]
)

# Agent 2: YAML Writer - creates GitHub Actions workflow based on codebase analysis
yaml_writer = Agent(
    name="YAML Writer",
    model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
    knowledge=codebaseKB(),
    search_knowledge=True,
    tools=[FileTools()],
    instructions=[
        "You are a GitHub Actions expert. Create a comprehensive CI/CD workflow YAML file based on the Project Analyzer's findings.",
        "Search the knowledge base if you need additional context about the codebase structure.",
        "Create the file at: .github/workflows/ci-cd.yml",
        "For Python projects, use 'uv' as the package manager for faster dependency installation.",
        "Structure the workflow with these jobs:",
        "  1. 'test' job: Install dependencies with uv, run tests with coverage",
        "  2. 'build' job: Build Docker image only if tests pass",
        "  3. 'push' job: Push to GitHub Container Registry (ghcr.io) only on main branch",
        "Use workflow triggers: on push to main branch and on pull requests.",
        "For Python with uv, use these steps:",
        "  - Install uv: pip install uv",
        "  - Sync dependencies: uv sync",
        "  - Run tests: uv run pytest (or the test command identified from the codebase)",
        "Include proper caching for uv (.venv directory) to speed up builds.",
        "Add environment variables: REGISTRY (ghcr.io), IMAGE_NAME (${{ github.repository }})",
        "Use secrets: ${{ secrets.GITHUB_TOKEN }} for authentication.",
        "Add proper job dependencies: build needs test, push needs build.",
        "If a Dockerfile exists in the codebase, use it. Otherwise, create appropriate Docker build steps.",
        "Tailor the workflow to the specific project structure found in the codebase.",
        "Save the complete workflow to .github/workflows/ci-cd.yml"
    ]
)

# Agent 3: Validator - validates YAML and checks against codebase
validator = Agent(
    name="YAML Validator",
    model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
    knowledge=codebaseKB(),
    search_knowledge=True,
    tools=[FileTools()],
    instructions=[
        "You are a YAML and GitHub Actions validation expert.",
        "Read the generated .github/workflows/ci-cd.yml file.",
        "Search the codebase knowledge base to verify the workflow matches the actual project structure.",
        "Validate YAML syntax: proper indentation (2 spaces), correct structure, valid keys.",
        "Verify GitHub Actions syntax: valid job names, step names, action versions.",
        "Check that all required steps are present:",
        "  - Checkout code (actions/checkout@v4)",
        "  - Setup language runtime (Python, Node.js, etc.) matching the codebase",
        "  - Install dependencies (with uv for Python) using the correct dependency files",
        "  - Run tests with commands that match the test framework in the codebase",
        "  - Build Docker image using the Dockerfile if it exists",
        "  - Push to container registry",
        "Verify the test commands match what's actually used in the project.",
        "Check job dependencies are correctly defined (needs: [job-name]).",
        "Ensure caching is properly configured for dependencies.",
        "Validate Docker-related steps match the project's Docker configuration.",
        "Cross-reference with the codebase to ensure all paths and commands are correct.",
        "If errors are found or mismatches with the codebase exist, fix them and save the corrected file.",
        "Provide a final validation report confirming the workflow is production-ready and matches the codebase."
    ]
)

# Create the CI/CD setup team
cicd_team = Team(
    name="CI/CD Setup Team",
    model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
    members=[project_analyzer, yaml_writer, validator],
    instructions=[
        "Work as a coordinated team to create a production-ready GitHub Actions CI/CD pipeline based on the actual codebase.",
        "Step 1: Project Analyzer must search the codebase knowledge base and thoroughly analyze the project structure and requirements.",
        "Step 2: YAML Writer creates the workflow file using uv for Python projects, tailored to the specific codebase structure.",
        "Step 3: Validator checks the workflow file against the codebase for accuracy and fixes any issues found.",
        "All agents should use the codebase knowledge base to ensure the CI/CD pipeline matches the actual project.",
        "Ensure the final workflow includes: testing, linting, Docker build, and deployment to GitHub Container Registry.",
        "The workflow must use modern best practices: uv for Python, proper caching, job dependencies, and security with secrets.",
        "The pipeline must be customized to the specific project found in the codebase, not a generic template."
    ]
)

# Use the team
cicd_team.print_response(
    "Create a GitHub Actions CI/CD pipeline based on our codebase that uses uv for dependency management, "
    "runs the appropriate tests, and deploys as a Docker container to GitHub Container Registry"
)