from train import codebaseKB
from agno.agent import Agent
from agno.team import Team
from agno.models.google import Gemini
from agno.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.tools.file import FileTools
from agno.knowledge.embedder.google import GeminiEmbedder


# Agent 1: Bug Analyzer - searches knowledge base for bug location
bug_analyzer = Agent(
    name="Bug Analyzer",
    model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
    knowledge=codebaseKB(),
    search_knowledge=True,
    instructions=[
        "Search the codebase knowledge base to find relevant files",
        "Analyze the bug description and locate where it occurs",
        "Identify the exact file path and code section causing the bug",
        "Explain what needs to be changed to fix it"
    ]
)

# Agent 2: Code Fixer - writes and saves the fix
code_fixer = Agent(
    name="Code Fixer",
    model=Gemini(id="gemini-2.5-pro", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
    tools=[FileTools()],
    instructions=[
        "Based on the bug analysis, write the code fix",
        "Use the file path provided by the Bug Analyzer",
        "Save the fixed code to the file",
        "Explain what changes were made"
    ]
)

# Agent 3: Syntax Checker - validates syntax
syntax_checker = Agent(
    name="Syntax Checker",
    model=Gemini(id="gemini-2.5-pro", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
    tools=[FileTools()],
    instructions=[
        "Read and check the syntax of the updated code",
        "If syntax errors exist, fix them and save again",
        "Confirm the code is syntactically correct"
    ]
)


bug_fix_team = Team(
    name="Bug Fix Team",
    model=Gemini(id="gemini-2.5-pro", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
    members=[bug_analyzer, code_fixer, syntax_checker],
    instructions=[
        "First, Bug Analyzer must search the knowledge base to find the bug location",
        "Then Code Fixer writes and saves the fix",
        "Finally Syntax Checker validates the code"
    ]
)

def fix_bug(bug_description):
    """
    Run the bug fix team with a specific bug description

    Args:
        bug_description (str): Description of the bug to fix
    """
    prompt = f"Analyze this bug description and fix it: {bug_description}, once you come up with a fix use the replace_file_chunk to write the fix."
    response = bug_fix_team.run(prompt)
    print(response.content)

# Use the team (for testing purposes)
# if __name__ == "__main__":
#     fix_bug("Find why I am getting a 2+2 output as 0, and fix it using the replace_file_chunk")
