from agno.agent import Agent
from agno.models.google import Gemini
from agno.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.tools.file import FileTools
from train import codebaseKB
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.shell import ShellTools
from dotenv import load_dotenv
load_dotenv()

def githubAgent(codeChanges):
    agent = Agent(
        model=Gemini(id="gemini-2.0-flash"),
        tools=[ShellTools()],
        instructions=[
            "You analyze git changes and create meaningful commit messages",
            "Use 'git add .' to stage all changes",
            "Create descriptive commit messages based on the code changes",
            "Run 'git commit -m \"message\"' with the generated message",
            "Finally run 'git push' to push changes"
        ],
        markdown=True
    )

    agent.print_response(f"Analyze the latest code changes and push them to GitHub with an appropriate commit message: {codeChanges}")