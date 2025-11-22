Below is a concrete example of taking a “classic” multi-hop RAG pipeline and rewriting it using `deepagents`.

I’ll keep it minimal but realistic and annotate what DeepAgents is buying you.

---

## Scenario

User question:

> “Explain how Azure AD Connect sync works and then compare it to Entra Cloud Sync.”

We want:

1. Break into sub-questions (multi-hop).
2. Retrieve docs for each sub-question.
3. Summarize each hop.
4. Produce a final comparison answer.

---

## Baseline: “Classic” Multi-Hop RAG (no DeepAgents)

This is the usual pattern you’ve seen:

```python
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

Write a concise summary (8–10 bullet points).
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
```

Limitations:

* All intermediate state lives in Python variables / inside prompts.
* No persistent memory, no filesystem, no graph.
* Harder to extend with more tools or sub-agents.

---

## DeepAgents Version: Multi-Hop RAG with Planning + FS

Now we wrap the same logic into a `DeepAgent` that:

* Plans sub-questions internally.
* Calls a retrieval tool multiple times.
* Writes intermediate results to files.
* Reads them back for final synthesis.

### 1. Setup

```python
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
```

### 2. Create the Deep Agent

Note: DeepAgents automatically gives you:

* `write_file`, `read_file`, `ls`, etc.
* Planning / TODO middleware.

```python
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

- First, think about 2–4 sub-questions needed to answer the question.
- Use `retrieve_docs` separately for each sub-question.
- After retrieving docs for a sub-question, write a summary file named
  `summary_<index>.txt`, where <index> is 1, 2, 3, ...

- Once all summaries are written, read them back and write a final
  answer into `final_answer.txt`.

When you are done, return ONLY the contents of `final_answer.txt`.
"""
)
```

### 3. Invoke DeepAgents as a Multi-Hop RAG Worker

```python
question = """
Explain how Azure AD Connect sync works and then compare it
to Entra Cloud Sync for a hybrid Azure AD environment.
"""

result = agent.invoke(question)
print(result["output"])  # final synthesized answer
```

---

## What DeepAgents Actually Does (Step-by-Step)

Inside `agent.invoke(...)`, the agent’s reasoning loop will look like this:

1. **Decomposition (multi-hop planning)**
   Agent internally creates a TODO list like:

   * Sub-Q1: “What is Azure AD Connect sync and how does it work?”
   * Sub-Q2: “What is Entra Cloud Sync and how does it work?”
   * Sub-Q3: “What are the differences between the two for hybrid environments?”

2. **Hop 1: Retrieval + summary**

   * Calls:

     ```text
     retrieve_docs("What is Azure AD Connect sync and how does it work?")
     ```
   * Receives a block of docs.
   * Writes summary:

     ```text
     write_file("summary_1.txt", "<bulleted summary>")
     ```

3. **Hop 2: Retrieval + summary**

   * Calls:

     ```text
     retrieve_docs("What is Entra Cloud Sync and how does it work?")
     ```
   * Writes:

     ```text
     write_file("summary_2.txt", "<bulleted summary>")
     ```

4. **Hop 3: Retrieval + summary**

   * Calls:

     ```text
     retrieve_docs("Differences between Azure AD Connect and Entra Cloud Sync")
     ```
   * Writes:

     ```text
     write_file("summary_3.txt", "<bulleted summary>")
     ```

5. **Final aggregation**

   * Reads all summaries:

     ```text
     s1 = read_file("summary_1.txt")
     s2 = read_file("summary_2.txt")
     s3 = read_file("summary_3.txt")
     ```

   * Produces final answer (comparison, pros/cons, maybe a table).

   * Writes:

     ```text
     write_file("final_answer.txt", "<full synthesis>")
     ```

   * Returns the content of `final_answer.txt` as `result["output"]`.

All the intermediate hops and files are preserved in the DeepAgents “workspace” (its internal FS). This is exactly the same multi-hop RAG logic, but now:

* It is **structured** (via files and implicit TODOs).
* It is **inspectable** (you can list / read all `summary_*.txt`).
* It is **extensible** (easy to add more tools and sub-agents).

---

## Why this is better than the bare multi-hop chain

From a pure algorithm perspective, you’re still doing:

* question → sub-questions → per-sub-question retrieval → summarize → synthesize.

But DeepAgents adds:

1. Explicit plan and steps (via TODO / planner).
2. Internal file system for intermediate artifacts.
3. Ability to add more tools later (e.g.,:

   * `internet_search`
   * `run_python`
   * `query_timeseries_db`
4. Easy extension to sub-agents:

   * “Architect sub-agent” for overall design.
   * “Security sub-agent” that only looks at security docs.
   * “Cost sub-agent” that looks at pricing and cost models.

The code you write stays almost the same, but the execution model becomes much richer.

---

If you want, I can next:

* Add a **second tool** (e.g., Azure REST docs web search) to this DeepAgents pipeline, or
* Show how to **spawn a “Cost Analysis” sub-agent** that reads the same summaries and produces a separate cost-focused section.
