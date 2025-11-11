from agno.knowledge.knowledge import Knowledge
from agno.vectordb.chroma import ChromaDb
from agno.knowledge.embedder.google import GeminiEmbedder

# Setup knowledge base with ChromaDB only (no SQL backend)
def bugReportknowledgeBase():
    knowledge = Knowledge(
        vector_db=ChromaDb(
            collection="csv_data",
            path="bugKB/chromadb",
            embedder=GeminiEmbedder(api_key="AIzaSyB7S3bAMC49oCDocCzIyOaDuEm-q8Gm8t0"),
            persistent_client=True
        ),

    )

    return knowledge

def retrainBugReportKB():
    knowledge = Knowledge(
        vector_db=ChromaDb(
            collection="csv_data",
            path="bugKB/chromadb",
            embedder=GeminiEmbedder(api_key="AIzaSyB7S3bAMC49oCDocCzIyOaDuEm-q8Gm8t0"),
            persistent_client=True
        )
    )

    knowledge.add_contents([{"path": "bug_reports.csv"}])

def codebaseKB():
    codebase = Knowledge(
        vector_db=ChromaDb(
            collection="sourcecode",
            path="codebase/chromadb",
            persistent_client=True,
            embedder=GeminiEmbedder(api_key="AIzaSyB7S3bAMC49oCDocCzIyOaDuEm-q8Gm8t0"),
        )
    )

    return codebase

def codebaseTrain():
    knowledge = Knowledge(
        vector_db=ChromaDb(
            collection="sourcecode",
            path="codebase/chromadb",
            persistent_client=True,
            embedder=GeminiEmbedder(api_key="AIzaSyB7S3bAMC49oCDocCzIyOaDuEm-q8Gm8t0"),
        )
    )

# # Add your codebase
#     knowledge.add_content(
#         name="Codebase",
#         path="/Users/arreyanhamid/Developer/aiResponder/test.py",
#         metadata={"type": "source_code"}
#     )

    # knowledge.add_content(
    #     path="/Users/arreyanhamid/Developer/aiResponder",
    #     include=["test.py"],  # Only Python files
    #     exclude=["*__pycache__*"]  # Skip test files and cache
    # )

    knowledge.add_contents([{"path": "test.py"}])

# codebaseTrain()
# Uncomment to run manually
# retrainBugReportKB()