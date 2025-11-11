from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini
from agno.tools.shell import ShellTools

# Agent 1: Git Committer - commits and pushes code to GitHub
git_committer = Agent(
    name="Git Committer",
    model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
    tools=[ShellTools()],
    instructions=[
        "Stage all changes using 'git add .'",
        "Commit changes with a descriptive message",
        "Push code to the main branch using 'git push origin main'",
        "Confirm the push was successful"
    ]
)

# Agent 2: GitHub Actions Monitor - checks workflow status
actions_monitor = Agent(
    name="GitHub Actions Monitor",
    model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
    tools=[ShellTools()],
    instructions=[
        "Use 'gh run list --limit 1' to check the latest workflow run",
        "Monitor the workflow status until completion",
        "Report if the deployment succeeded or failed",
        "If failed, provide error details"
    ]
)

# Agent 3: Deployment Verifier - confirms deployment
deployment_verifier = Agent(
    name="Deployment Verifier",
    model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
    tools=[ShellTools()],
    instructions=[
        "Verify the deployment was successful",
        "Check if the application is running correctly",
        "Provide a final deployment report"
    ]
)

# Create the deployment team
deployment_team = Team(
    name="GitHub Deployment Team",
    model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
    members=[git_committer, actions_monitor, deployment_verifier],
    instructions=[
        "First, commit and push code to GitHub",
        "Then monitor the GitHub Actions workflow",
        "Finally verify the deployment succeeded"
    ]
)

# Deploy the code
deployment_team.print_response("Deploy the latest bug fixes to production")