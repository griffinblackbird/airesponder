from agno.agent import Agent
from agno.models.google import Gemini
from agno.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.tools.file import FileTools
from train import codebaseKB

# Single CI/CD Agent - analyzes codebase and creates deployment workflow
cicd_agent = Agent(
    name="CI/CD Agent",
    model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
    knowledge=codebaseKB(),
    search_knowledge=True,
    tools=[FileTools()],
    instructions=[
        "You are a DevOps expert specializing in GitHub Actions and Docker deployments.",
        "Use python 3.11.13 ONLY",
        "Search the codebase knowledge base to understand the project structure.",
        "Look for: pyproject.toml, requirements.txt, package.json, Dockerfile, or similar files.",
        "Identify the programming language and dependencies.",
        "Create a GitHub Actions workflow file at .github/workflows/deploy.yml that:",
        "  - Triggers on push to main branch",
        "  - Checks out the code",
        "  - Sets up the appropriate language runtime",
        "  - Installs dependencies (use uv for Python projects - pip install uv followed by uv venv followed by uv add -r requirements.txt)",
        "  - Builds a Docker image, the image name should be LOWERCASE",
        "  - Pushes the image to GitHub Container Registry (ghcr.io)",
        "Use proper caching for faster builds.",
        "Use ${{ secrets.GITHUB_TOKEN }} for authentication.",
        "Set environment variables: REGISTRY=ghcr.io, IMAGE_NAME=${{ github.repository }}",
        "Ensure the workflow is valid YAML with proper indentation.",
        "Save the workflow file to .github/workflows/deploy.yml"
    ]
)

# Use the agent
cicd_agent.print_response(
    "Create a GitHub Actions workflow that builds and deploys the code as a Docker container to GitHub Container Registry"
)