Yes — **besides “system”, “developer”, and “user”**, modern LLMs (OpenAI, Azure OpenAI, Anthropic, etc.) support **additional message roles**, depending on the API version.

Here is the complete list.

---

# ✅ **1. system**

Defines the model’s identity, policies, tone, behavior boundaries.

---

# ✅ **2. developer**

Medium-priority control layer (above user).
For workflow logic, formatting, app-level constraints.

---

# ✅ **3. user**

End-user request.
Lowest priority.

---

# 🟦 **4. assistant**

This is the model’s own previous replies.
Used to maintain conversation history.

You usually don’t manually write these — they come from the model — but you *can* insert them (e.g., in conversation replay or multi-agent routing).

---

# 🟧 **5. tool / function (OpenAI Function Calling)**

Used when the LLM triggers a function call.

Example:

```json
{ "role": "assistant", "tool_calls": [...] }
```

Then the developer code responds with:

```json
{ "role": "tool", "content": "...function output..." }
```

This is essential in:

* RAG pipelines
* Agents
* Multi-step workflows
* LangChain, LangGraph, DeepAgents apps

---

# 🟩 **6. tool_result / function_result**

After a function runs, your code returns:

```json
{
  "role": "tool",
  "tool_name": "search_database",
  "content": "{...result...}"
}
```

Some APIs call this:

* `"tool"`
* `"function"`
* `"assistant_tool"`
* `"tool_result"`

Used to feed tool output back into the model.

---

# 🟫 **7. assistant with refusal**

OpenAI has special system metadata for safety refusals:

```json
{ "role": "assistant", "refusal": {...} }
```

You rarely use this manually.

---

# 🟨 **8. assistant with thinking (hidden chain-of-thought)**

Models internally generate:

* reasoning
* planning
* decomposition

But **this is hidden** and not exposed in API responses.

Not accessible to developers.

---

# 🟪 **9. additional metadata roles**

These depend on platform:

### OpenAI / Azure

* `"system"`
* `"developer"`
* `"user"`
* `"assistant"`
* `"tool"`

### Anthropic

* `"system"`
* `"user"`
* `"assistant"`
* `"tool"`

### Google Gemini

* `"system"`
* `"user"`
* `"model"`

---

# 🌐 **Complete Role Map (OpenAI GPT-4.1 / GPT-4o)**

| Role                       | Purpose                                   |
| -------------------------- | ----------------------------------------- |
| **system**                 | Global identity + top-level rules         |
| **developer**              | App logic / workflow rules                |
| **user**                   | User query                                |
| **assistant**              | LLM answer history                        |
| **tool**                   | Output of a tool/function                 |
| **assistant (tool_calls)** | LLM triggering tools                      |
| **tool_result**            | Tool execution results (depending on API) |

These are **all** the roles that matter for building LLM apps today.

---

# 🧪 **Do you want an example?**

I can show you a **full Python example** using:

* system
* developer
* user
* assistant
* tool
* tool_result

🔥 With multi-step reasoning + tool calling + RAG + function calling.

Just tell me: **“show the full example”**.


Below is a **single, self-contained Python example** that shows:

* `system` role
* `developer` role
* `user` role
* `assistant` role (history)
* `tool` role (this is where the “tool_result” lives)
* Multi-step reasoning via **function calling + RAG-style retrieval**

It uses:

* A fake **RAG tool**: `search_knowledge_base`
* A fake **calculator tool**: `math_tool`
* OpenAI **function calling** (`tools`) with the modern Python SDK (`openai>=1.x` style)

You can adapt this directly for real vector DB / HTTP tools.

---

```python
"""
Multi-step reasoning + tool calling + RAG + all roles:
- system
- developer
- user
- assistant
- tool (used as the "tool_result" container)
"""

from openai import OpenAI
import json

client = OpenAI()

# -------------------------------
# Fake "RAG" knowledge base and tools
# -------------------------------

DOCUMENTS = [
    {
        "id": "doc-1",
        "title": "LLM Systems Overview",
        "content": "Retrieval-Augmented Generation (RAG) combines an LLM with a vector store."
    },
    {
        "id": "doc-2",
        "title": "Tools and Function Calling",
        "content": "LLMs can call tools such as web search or databases via structured function calls."
    },
    {
        "id": "doc-3",
        "title": "Multi-Agent Systems",
        "content": "Multi-agent LLM systems can use planners, retrievers, and evaluators in sequence."
    },
]

def search_knowledge_base(query: str, top_k: int = 2):
    """
    Very simple fake RAG: return the 'most relevant' docs
    (here just the first top_k for demo).
    """
    results = DOCUMENTS[:top_k]
    return {
        "query": query,
        "results": results,
    }

def math_tool(expression: str):
    """
    Very simple math tool that evals a safe arithmetic expression.
    DO NOT use eval in production – this is only for demo.
    """
    try:
        # Extremely limited example: only digits and operators
        if not all(c in "0123456789+-*/(). " for c in expression):
            raise ValueError("Unsafe expression.")
        value = eval(expression)
        return {"expression": expression, "result": value}
    except Exception as e:
        return {"expression": expression, "error": str(e)}


# -------------------------------
# Tool schema for OpenAI function calling
# -------------------------------

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_knowledge_base",
            "description": "Searches the internal knowledge base for relevant documents (RAG).",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "top_k": {"type": "integer", "default": 2},
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "math_tool",
            "description": "Evaluate a simple math expression like '2+2*3'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string"},
                },
                "required": ["expression"],
            },
        },
    },
]


# -------------------------------
# Conversation setup (all roles)
# -------------------------------
# system   -> global rules / identity
# developer-> app-level rules (formatting, behavior)
# user     -> user question
# assistant-> previous AI response (history)
# tool     -> tool_result messages

messages = [
    {
        "role": "system",
        "content": (
            "You are a senior LLM engineer assistant. "
            "You must reason step-by-step internally and use tools when helpful. "
            "When answering, be concise and structured."
        ),
    },
    {
        "role": "developer",
        "content": (
            "Always answer in Markdown with sections:\n"
            "1. Thought process (high level, no chain-of-thought)\n"
            "2. Answer\n"
            "3. Sources (if tools used)"
        ),
    },
    # Example previous assistant message (history)
    {
        "role": "assistant",
        "content": "Hello, I can help you design LLM systems with tools and RAG.",
    },
    # Actual user query
    {
        "role": "user",
        "content": (
            "I have an LLM app. Explain how multi-step reasoning with RAG and a math tool "
            "could work together to answer: "
            "'Use the docs to explain RAG briefly, then compute 12 * (5 + 3)'."
        ),
    },
]


# -------------------------------
# Main loop: multi-step reasoning + tool calling
# -------------------------------

def run_conversation():
    """
    Orchestrates a conversation:
    - model may call tools (RAG + math)
    - we execute tools and feed back tool_result as role='tool'
    - we loop until model stops calling tools
    """

    global messages

    while True:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto",
        )

        msg = response.choices[0].message

        # Append assistant message to history (role='assistant')
        messages.append(
            {
                "role": "assistant",
                "content": msg.content or "",
                "tool_calls": msg.tool_calls or None,
            }
        )

        # If no tool calls, we are done – final answer is msg.content
        if not msg.tool_calls:
            print("FINAL ASSISTANT ANSWER:\n")
            print(msg.content)
            break

        # Otherwise, handle each tool call (multi-step)
        for tool_call in msg.tool_calls:
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments or "{}")

            if tool_name == "search_knowledge_base":
                tool_output = search_knowledge_base(**tool_args)
            elif tool_name == "math_tool":
                tool_output = math_tool(**tool_args)
            else:
                tool_output = {"error": f"Unknown tool {tool_name}"}

            # Now we append a tool_result message with role='tool'
            # This is what you referred to as "tool_result".
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": json.dumps(tool_output),
                }
            )

        # Loop continues: the model will see both the assistant message
        # and the tool_result messages and can reason further or finalize.


if __name__ == "__main__":
    run_conversation()
```

---

### How this satisfies your requirements

* **system**
  Top-level message in `messages[0]`.

* **developer**
  Second message in `messages[1]` with formatting & behavior rules.

* **assistant**

  * A prior assistant message for history (`"Hello, I can help you..."`).
  * New assistant messages from the model appended in the loop.

* **user**
  The real question about *multi-step reasoning with RAG + math*.

* **tool**
  When tools are executed, we append messages with `role="tool"` and `tool_call_id` – this is effectively the **“tool_result”** channel.

* **Multi-step reasoning + RAG + function calling**
  The model:

  1. Reads the user request.
  2. May call `search_knowledge_base` (RAG) to get documents.
  3. May call `math_tool` to evaluate `12 * (5 + 3)`.
  4. Sees tool results (role='tool') and synthesizes a final answer.

If you tell me your **actual stack** (e.g., Azure OpenAI vs OpenAI, LangChain vs bare API, your existing RAG store), I can adapt this example to your exact environment (including async, FastAPI, etc.).
