# from agno.knowledge.knowledge import Knowledge
# from agno.vectordb.chroma import ChromaDb
# from agno.knowledge.embedder.google import GeminiEmbedder
# from agno.agent import Agent
# from agno.models.google import Gemini
# from agno.db.sqlite import SqliteDb

# contents_db = SqliteDb(
#     db_file="tmp/knowledge.db",
#     knowledge_table="knowledge_contents"
# )

# # Create knowledge base with ChromaDB
# knowledge = Knowledge(
#     vector_db=ChromaDb(
#         collection="codebase",
#         path="tmp/chromadb",
#         embedder=GeminiEmbedder(api_key="AIzaSyAZgqVCD8JAZggnZv7f2z_hHAPBcnRPoDs"),
#         persistent_client=True
#     ),
#     contents_db=contents_db

# )
# # Add your files
# knowledge.add_contents([
#     {"path": "student_template.csv"},
# ])


# print(knowledge.get_content())

# agent = Agent(
#     model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyAZgqVCD8JAZggnZv7f2z_hHAPBcnRPoDs"),

#     knowledge=knowledge,
#     instructions=[
#         "Always search your knowledge base before answering.",
#         "Use the search_knowledge_base tool to find relevant information."
#     ],
#     search_knowledge=True,
#     markdown=True
# )

# # Query the codebase
# agent.print_response("What is the email and phone number of Jacob?")

from agno.agent import Agent
from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.models.google import Gemini
from agno.knowledge.embedder.google import GeminiEmbedder
from train import bugReportknowledgeBase
from pydantic import BaseModel, Field
import pandas as pd
import os

class BugReport(BaseModel):
    similarity_status: str = Field(description="Either 'Similar query found' or 'Unique query'")
    priority: str = Field(description="Priority level: high, medium, or low")
    similar_entry: str = Field(default="", description="The similar entry if found")

def updateSeverityScore(service_number, severity_score):
    """Update the severity score for a specific bug report"""
    if not os.path.exists('bug_reports.csv'):
        return False

    try:
        df = pd.read_csv('bug_reports.csv')

        if service_number in df['service_number'].values:
            # Convert severity_score column to string type to handle nan values
            df['severity_score'] = df['severity_score'].astype(str)

            # Update the severity score
            df.loc[df['service_number'] == service_number, 'severity_score'] = severity_score
            df.to_csv('bug_reports.csv', index=False)
            return True
        else:
            return False

    except Exception as e:
        return False

def similaritySearch(newBug):
    """Search for similar bugs and return priority"""
    print(f"🔍 similaritySearch called")

    try:
        print("🤖 Starting AI agent...")
        agent = Agent(
            model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyCweEU4x5aVyNSQFiD9AvotzkV8BUEmrng"),
            knowledge=bugReportknowledgeBase(),
            search_knowledge=True,
            instructions=[
                "Search the knowledge base for similar entries.",
                "If found, return the similar query and set similarity_status to 'Similar query found'.",
                "If not found, set similarity_status to 'Unique query'.",
                "Always assign a priority: high, medium, or low based on severity."
            ],
            output_schema=BugReport,
            markdown=True
        )

        print(f"📝 Running agent with query: {newBug}")
        response = agent.run(f"Check if this entry exists: {newBug}")
        print(response.content)
        print(f"✅ Agent completed successfully")

        # Extract priority from the response
        priority = "unknown"
        if hasattr(response, 'content') and hasattr(response.content, 'priority'):
            priority = response.content.priority
            print(f"🎯 Extracted priority from response.content.priority: {priority}")
        else:
            priority = str(response.content)
            print(f"🎯 Converted response to string: {priority}")

        print(f"🎯 Final priority: {priority}")
        return priority

    except Exception as e:
        print(f"❌ Error in similarity search: {str(e)}")
        import traceback
        traceback.print_exc()
        return "error"

def ensureSeverityColumn():
    """Ensure severity_score column exists in bug_reports.csv"""
    if os.path.exists('bug_reports.csv'):
        df = pd.read_csv('bug_reports.csv')

        if 'severity_score' not in df.columns:
            df['severity_score'] = ''
            df.to_csv('bug_reports.csv', index=False)
            print("Added severity_score column to bug_reports.csv")

        return True
    else:
        print("bug_reports.csv does not exist")
        return False

# Initialize the severity column if it doesn't exist
if __name__ == "__main__":
    ensureSeverityColumn()

    # Example usage:
    # similaritySearch(newBug="my name is john", service_number="SR-20251110-ABCDEF123")