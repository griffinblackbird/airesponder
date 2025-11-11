from agno.agent import Agent
from train import codebaseKB
from agno.models.google import Gemini
from agno.tools.file import FileTools
from pathlib import Path
from agno.models.groq import Groq
from agno.team import Team

# # Create debugging agent
# # agent = Agent(
# #     # model=Ollama(id="codellama:7b"),
# #     model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyCweEU4x5aVyNSQFiD9AvotzkV8BUEmrng"),
# #     knowledge=codebaseKB(),
# #     search_knowledge=True,
# #     instructions=[
# #         "You are a code debugging expert",
# #         "Search the codebase to find relevant code sections",
# #         "Analyze errors and trace them to exact file locations",
# #         "Provide specific file paths and line numbers"
# #     ]
# # )

# agent = Agent(
#     model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyCweEU4x5aVyNSQFiD9AvotzkV8BUEmrng"),
#     knowledge=codebaseKB(),
#     search_knowledge=True,
#     tools=[FileTools(base_dir=Path("/Users/arreyanhamid/Developer/aiResponder/test.py"))],  # Add FileTools
#     instructions=[
#         "You are a code debugging expert",
#         "Search the codebase to find bugs",
#         "Analyze errors and provide fixes",
#         "After identifying the fix, AUTOMATICALLY write it to the file using save_file",
#         "Provide the exact file path and explain the changes made"
#     ]
# )
# # Use the agent
# agent.print_response(
#     "Find why I am getting a 2+2 output as 0.",
#     markdown=True
# )


# Set your codebase path
# CODEBASE_PATH = "/Users/arreyanhamid/Developer/aiResponder"


# # Create debugging agent with file writing capability
# agent = Agent(
#     model=Groq(id="llama-3.3-70b-versatile", api_key="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"),
#     knowledge=codebaseKB(),
#     search_knowledge=True,  # Enables agentic RAG
#     tools=[FileTools(base_dir=Path(CODEBASE_PATH))],  # Add file writing
#     instructions=[
#         "You are an expert code debugger",
#         "Search the knowledge base to find relevant code and bugs",
#         "Analyze errors and identify the exact file and location",
#         "Generate the corrected code",
#         "AUTOMATICALLY save the fix using save_file tool",
#         "Provide clear explanation of what was fixed, and make sure the update code has the correct syntax and works fine."
#     ],
#     markdown=True
# )

# # Use the agent - it will find, fix, and save automatically
# agent.print_response(
#     "Find why I am getting a 2+2 output as 0, and fix it",
#     markdown=True
# )

# Agent 1: Bug Analyzer - finds where the bug is
# bug_analyzer = Agent(
#     name="Bug Analyzer",
#     model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
#     knowledge=codebaseKB(),
#     search_knowledge=True,
#     instructions=[
#         "Analyze the bug description and search the codebase",
#         "Identify exactly where in the code the bug is occurring",
#         "Explain what needs to be changed to fix it"
#     ]
# )

# # Agent 2: Code Fixer - writes the fix and saves it
# code_fixer = Agent(
#     name="Code Fixer",
#     model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
#     tools=[FileTools()],
#     instructions=[
#         "Based on the bug analysis, write the code fix",
#         "Save the fixed code to the appropriate file",
#         "Explain what changes were made"
#     ]
# )

# # Agent 3: Syntax Checker - validates and fixes syntax
# syntax_checker = Agent(
#     name="Syntax Checker",
#     model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
#     tools=[FileTools()],
#     instructions=[
#         "Check the syntax of the updated code",
#         "If syntax errors exist, fix them and save the file again",
#         "Confirm the code is syntactically correct"
#     ]
# )

# # Create the bug-fixing team
# bug_fix_team = Team(
#     name="Bug Fix Team",
#     model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
#     members=[bug_analyzer, code_fixer, syntax_checker],
#     instructions=[
#         "Work together to fix bugs in the codebase",
#         "First analyze and locate the bug",
#         "Then write and save the fix",
#         "Finally validate the syntax"
#     ]
# )

# # Use the team
# bug_fix_team.print_response("Find why I am getting a 2+2 output as 0, and fix it using the replace_file_chunk")

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
    model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
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
    model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
    tools=[FileTools()],
    instructions=[
        "Read and check the syntax of the updated code",
        "If syntax errors exist, fix them and save again",
        "Confirm the code is syntactically correct"
    ]
)

# Create the bug-fixing team
bug_fix_team = Team(
    name="Bug Fix Team",
    model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyDLMFmE0yQM_9an5LHX-J3AQw3mpgPb0To"),
    members=[bug_analyzer, code_fixer, syntax_checker],
    instructions=[
        "First, Bug Analyzer must search the knowledge base to find the bug location",
        "Then Code Fixer writes and saves the fix",
        "Finally Syntax Checker validates the code"
    ]
)

# Use the team
bug_fix_team.print_response("Find why I am getting a 2+2 output as 0, and fix it using the replace_file_chunk")
