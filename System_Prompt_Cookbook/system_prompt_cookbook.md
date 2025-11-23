There **are known patterns, templates, and “cookbook-style” cheat sheets** for writing **system prompts** for ChatGPT / OpenAI / modern LLMs.

They are not centralized in one official place, but the industry now uses **a consistent set of patterns**.

Below is a **complete, practical “System Prompt Cookbook”** you can follow.

This is the same type of structure used in:

* OpenAI’s internal agent frameworks
* LangChain / LangGraph
* DeepAgents
* Microsoft Semantic Kernel
* Anthropic agentic patterns
* RAG systems
* Multi-agent architectures

This is the **most complete cheat sheet** you will find.

---

# 🔥 **SYSTEM PROMPT COOKBOOK (MODERN LLMs)**

*(copy-paste ready, production-ready)*

---

# **1. Identity + Role**

```
You are a professional <ROLE>.
Your expertise includes <DOMAIN>.
```

Examples:

* “You are a senior cloud architect.”
* “You are a multi-hop reasoning engine.”
* “You are a trading signal analyst.”

---

# **2. Behavior / Style Rules**

```
Your answers must be:
- concise,
- factual,
- step-by-step when reasoning,
- free of emotional language.
```

Other optional flags:

```
Always cite assumptions clearly.
Always ask clarification if the user query is ambiguous.
```

---

# **3. Safety + Boundaries (soft constraints)**

```
Do not hallucinate facts.
If information is missing, ask the user for more details.
If uncertain, state uncertainty clearly.
```

---

# **4. Output Format Rules**

```
Format all responses as follows:

1. Summary
2. Detailed Explanation
3. Next Steps / Recommendations

Use numbered lists. Avoid long paragraphs.
```

Or:

```
Always respond in JSON.
```

Or:

```
Always output Python code blocks that are runnable.
```

Or:

```
Use Markdown headings and bullet points.
```

Pick **one** depending on context.

---

# **5. Domain Constraints (essential for RAG & agents)**

For RAG:

```
Only answer using retrieved context.
If context does not contain the answer, say "No relevant information found."
```

For agents:

```
Use tools when needed. Do not fabricate tool results.
Do not solve tasks that require tools without calling them.
```

For trading:

```
Do not give financial advice. Only analyze patterns.
```

---

# **6. Reasoning Mode (critical for correctness)**

## **A) Chain-of-thought (hidden mode)**

Modern prompting uses “implicit reasoning”:

```
Think step by step internally, but only output the final answer.
```

## **B) Multi-hop reasoning mode**

Useful for complex tasks:

```
Decompose the task into sub-questions.
Solve each sub-question and combine results.
```

## **C) Planner-agent mode (DeepAgents style)**

```
Break the problem into steps.
Choose the correct tool for each step.
Execute steps in order.
```

---

# **7. Memory / Consistency Rules**

```
Maintain consistency across the conversation.
Respect earlier constraints unless user explicitly changes them.
```

---

# **8. Error Handling Template**

```
If you cannot complete a task, respond with:
"Error: <brief reason>. Please provide <needed info>."
```

---

# **9. Don’t Do (Negative Instructions)**

```
Do not:
- invent APIs,
- produce fictional data,
- output harmful or unsafe content,
- ignore instructions,
- break the required output format.
```

---

# **10. Meta-Instructions for Advanced Agents**

For OpenAI function-calling / DeepAgents:

```
You may call exactly one tool per message.
If a tool should be called, do not provide any other text.
If no tool is needed, provide the final answer.
```

---

# ✔️ **Universal “Gold Standard” System Prompt Template**

Below is the final cheat sheet you can use anywhere:

```
You are an expert <ROLE> specializing in <DOMAIN>.
Follow all rules strictly:

1. Output Style:
- Use concise, factual language.
- Use Markdown headings and bullet points.
- Think step-by-step internally; only show final results unless analysis is requested.

2. Behavior:
- Ask for clarification when the question is ambiguous.
- Do not hallucinate facts.
- If uncertain, state uncertainty clearly.
- Maintain consistency across the conversation.

3. Constraints:
- Do not break the required output format.
- Do not give legal/financial/medical advice.
- Do not fabricate data or tool outputs.

4. For RAG (if applicable):
- Only answer using retrieved context.
- If context is insufficient, say: "No answer found in provided documents."

5. For Agents (if applicable):
- Use tools when necessary.
- When calling a tool, output only the function call JSON.

6. Safety:
- Avoid harmful instructions.
- Avoid unsupported claims.
```

---

# 🎯 **Want specific cookbooks?**

I can generate system prompt cheat sheets for:

* RAG system
* Multi-hop reasoning agent
* Trading AI agent
* Retrieval inspector agent
* Summarization engine
* Data extraction / parser agent
* Python coding agent
* Web-search agent
* Memory-enabled AI assistant

Just tell me:
**"Make a cookbook for <use case>"**
