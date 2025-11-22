# step 1: Setup

from langchain_openai import ChatOpenAI
from langchain.tools import tool
from deepagents import DeepAgent

# Same vector_store as before
vector_store = ...  # your FAISS / Chroma / etc.

@tool
def retrieve_docs(query: str):
    """Retrieve relevant docs from the Azure knowledge base."""
    docs = vector_store.similarity_search(query, k=5)
    return "\n\n".join(d.page_content for d in docs)

llm = ChatOpenAI(model="gpt-4.1")



# step 2:Create the Deep Agent

agent = DeepAgent(
    model=llm,
    tools=[retrieve_docs],   # plus built-in FS tools
    system_prompt="""
You are a multi-hop RAG research agent.

Goal:
Given a user question, you must:
1. Decompose it into sub-questions.
2. For each sub-question, call `retrieve_docs`.
3. Summarize each retrieval result.
4. Save all summaries into files.
5. Read all summaries and write a final synthesized answer.

Use the following strategy:

- First, think about 2-4 sub-questions needed to answer the question.
- Use `retrieve_docs` separately for each sub-question.
- After retrieving docs for a sub-question, write a summary file named
  `summary_<index>.txt`, where <index> is 1, 2, 3, ...

- Once all summaries are written, read them back and write a final
  answer into `final_answer.txt`.

When you are done, return ONLY the contents of `final_answer.txt`.
"""
)


# step 3: Invoke DeepAgents as a Multi-Hop RAG Worker
question = """
Explain how Azure AD Connect sync works and then compare it
to Entra Cloud Sync for a hybrid Azure AD environment.
"""

result = agent.invoke(question)
print(result["output"])  # final synthesized answer
