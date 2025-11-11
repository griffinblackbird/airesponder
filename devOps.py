# from agno.agent import Agent
# from agno.team import Team
# from agno.models.google import Gemini
# from agno.tools.shell import ShellTools

# # Agent 1: Git Committer - commits and pushes code to GitHub
# git_committer = Agent(
#     name="Git Committer",
#     model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
#     tools=[ShellTools()],
#     instructions=[
#         "Stage all changes using 'git add .'",
#         "Commit changes with a descriptive message",
#         "Push code to the main branch using 'git push origin main'",
#         "Confirm the push was successful"
#     ]
# )

# # Agent 2: GitHub Actions Monitor - checks workflow status
# actions_monitor = Agent(
#     name="GitHub Actions Monitor",
#     model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
#     tools=[ShellTools()],
#     instructions=[
#         "Use 'gh run list --limit 1' to check the latest workflow run",
#         "Monitor the workflow status until completion",
#         "Report if the deployment succeeded or failed",
#         "If failed, provide error details"
#     ]
# )

# # Agent 3: Deployment Verifier - confirms deployment
# deployment_verifier = Agent(
#     name="Deployment Verifier",
#     model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
#     tools=[ShellTools()],
#     instructions=[
#         "Verify the deployment was successful",
#         "Check if the application is running correctly",
#         "Provide a final deployment report"
#     ]
# )

# # Create the deployment team
# deployment_team = Team(
#     name="GitHub Deployment Team",
#     model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
#     members=[git_committer, actions_monitor, deployment_verifier],
#     instructions=[
#         "First, commit and push code to GitHub",
#         "Then monitor the GitHub Actions workflow",
#         "Finally verify the deployment succeeded"
#     ]
# )

# # Deploy the code
# deployment_team.print_response("Deploy the latest bug fixes to production")

from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini
from agno.tools.file import FileTools

# Agent 1: Project Analyzer - analyzes project structure and requirements
project_analyzer = Agent(
    name="Project Analyzer",
    model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
    tools=[FileTools()],
    instructions=[
        "Analyze the project structure to determine the programming language and framework",
        "Identify test commands, dependencies, and build requirements",
        "Determine the appropriate Docker base image and build steps",
        "Provide a summary of project requirements for CI/CD"
    ]
)

# Agent 2: YAML Writer - creates the GitHub Actions workflow file
yaml_writer = Agent(
    name="YAML Writer",
    model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
    tools=[FileTools()],
    instructions=[
        "Create a GitHub Actions workflow YAML file at .github/workflows/ci-cd.yml",
        "Include steps for: checkout, dependency installation, testing, Docker build, and push to GitHub Container Registry",
        "Add proper environment variables and secrets configuration",
        "Ensure the workflow runs on push to main and pull requests",
        "Save the file to .github/workflows/ci-cd.yml"
    ]
)

# Agent 3: Validator - validates the YAML syntax and configuration
validator = Agent(
    name="YAML Validator",
    model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
    tools=[FileTools()],
    instructions=[
        "Read and validate the GitHub Actions YAML file",
        "Check for syntax errors, proper indentation, and valid GitHub Actions syntax",
        "Verify all required steps are present: test, build, push",
        "If errors exist, fix them and save the corrected file",
        "Confirm the workflow is valid and ready to use"
    ]
)

# Create the CI/CD setup team
cicd_team = Team(
    name="CI/CD Setup Team",
    model=Gemini(id="gemini-2.5-pro", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
    members=[project_analyzer, yaml_writer, validator],
    instructions=[
        "First, analyze the project to understand its requirements",
        "Then create a comprehensive GitHub Actions workflow file",
        "Finally validate and fix any issues in the workflow file"
    ]
)

# Use the team
cicd_team.print_response("Create a GitHub Actions CI/CD pipeline that tests the project and deploys it as a Docker container to GitHub Container Registry")