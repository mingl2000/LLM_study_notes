from langchain_openai import ChatOpenAI
from langchain.tools import tool

# Assume you have an existing vector store with Azure docs
vector_store = ...  # e.g., FAISS / Chroma

llm = ChatOpenAI(model="gpt-4.1")

@tool
def retrieve_docs(query: str):
    """Retrieve relevant docs from the Azure knowledge base."""
    docs = vector_store.similarity_search(query, k=5)
    return "\n\n".join(d.page_content for d in docs)

def multi_hop_rag(question: str):
    # 1) Ask LLM to propose sub-questions (hop planning)
    sub_qs = llm.invoke(
        f"""
You are a helpful assistant. Decompose this question into 2–4 sub-questions
that should be answered via document retrieval:

Question: {question}
Return each sub-question on its own line.
"""
    ).content.splitlines()

    # 2) For each sub-question: retrieve + local summary
    partial_summaries = []
    for sq in sub_qs:
        context = retrieve_docs.invoke({"query": sq})
        summary = llm.invoke(
            f"""
You are summarizing docs for sub-question: {sq}

Docs:
{context}

Write a concise summary (8-10 bullet points).
"""
        ).content
        partial_summaries.append((sq, summary))

    # 3) Final synthesis
    combined = "\n\n".join(
        f"Sub-question: {sq}\nSummary:\n{sm}" for sq, sm in partial_summaries
    )
    final_answer = llm.invoke(
        f"""
Original question:
{question}

You are given summaries for each sub-question:
{combined}

Write a final, structured answer.
Include a comparison table at the end.
"""
    ).content

    return final_answer
