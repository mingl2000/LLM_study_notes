Below is a **clean, structured overview** of the major **Python libraries/packages for LLM-related tasks**, grouped by what they help you do.
This is the **best high-level map** of the entire ecosystem.

I exclude tiny or low-quality packages.
Only real, widely-used, production-ready options.

---

# **1. Model Access (LLM Inference Clients)**

Packages that give you direct API access to commercial or open-source models.

## **OpenAI / Azure OpenAI**

* `openai`
* `openai` (Azure-compatible with `OpenAI(api_key=..., base_url=...)`)

## **Anthropic Claude**

* `anthropic`

## **Google Gemini / Vertex**

* `google-generativeai`

## **Cohere**

* `cohere`

## **Mistral**

* `mistralai`

## **Open Source Models (local or hosted)**

* **Ollama** → `ollama`
* **vLLM** → `vllm`
* **HF Transformers** → `transformers`
* **Text Generation Inference (TGI)** → `huggingface_hub`, `text-generation`

---

# **2. High-Level LLM Frameworks (Agents, Chains, RAG)**

These packages orchestrate reasoning, tools, retrieval, memory, agents, and workflows.

## **Modern, Production Tooling**

### 1) **LangChain**

* `langchain` (v1)
* `langchain_core`
* `langchain_community`
* `langgraph` (workflow engine)
* `deepagents` (advanced agent framework)

### 2) **LlamaIndex**

* Unified RAG pipelines
* Indexing / document ingestion / context engines
* Agents with tools & workflows

### 3) **Haystack**

* Enterprise-grade search + RAG
* Elasticsearch / FAISS integration
* Pipelines & nodes

### 4) **Semantic Kernel**

* .NET-first, Python supported
* Memories, skills, planners

### 5) **Guidance / Outlines**

* Controlled generation (templates + constraints)

---

# **3. RAG Components (Vector Stores, Embeddings, Retrieval)**

## **Vector Databases (Python client packages)**

* `faiss` or `faiss-gpu`
* `chromadb`
* `weaviate-client`
* `qdrant-client`
* `milvus` / `pymilvus`
* `pinecone-client`
* `redis` (Redis Vector Search)
* `elastic-enterprise-search`

## **Embedding Libraries**

* `sentence-transformers` (SBERT family)
* `huggingface_hub`
* `openai` (text-embedding models)
* `voyageai`
* `cohere`

## **Document Loaders**

* `langchain_community.document_loaders`
* `llama-index-readers`
* `pypdf`
* `docx2txt`
* `pdfplumber`

---

# **4. Agents, Tools, Multi-Step Reasoning**

## **Agent Frameworks**

* **deepagents**
  Multi-step planning + sub-agents + file system + memory (best modern agent framework).
* **LangGraph**
  State-machine graph for complex agent workflows.
* **LangChain Agents**
  Tools, planning, execution loops.
* **LlamaIndex Agents**
  Simpler but strong in RAG contexts.

## **Tool / Function Calling libraries**

* `openai` function calling
* `pydantic` schemas
* `jsonref`, `jsonschema`
* `lark`, `antlr4-python3-runtime` (grammar-based parsing)

---

# **5. Prompting, Templates, and Guardrails**

## **Prompt libraries**

* `prompt_toolkit`
* `jinja2` (template-based prompting)
* `langchain` PromptTemplates
* `guidance` (template + control)
* `outlines` (probabilistic constraints)

## **Safety / Guardrails**

* `guardrails-ai`
* `nemoguardrails`
* `outlines` (structured output constraints)
* `flyswatter` (adversarial test prompts)

---

# **6. Evaluation & Testing (LLM QA, Benchmarks)**

## **Eval frameworks**

* **Ragas** → RAG evaluation
* **DeepEval** → structured LLM evaluation
* **TruLens** → trace + eval for LangChain/LlamaIndex apps
* **Gorilla Evals**
* **OpenAI Evals**

## **Datasets**

* `datasets` (HuggingFace datasets)
* `ragas` synthetic QA generation

---

# **7. Data Processing & Preprocessing**

## **Document processing**

* `pypdf`, `pdfplumber`
* `python-docx`
* `beautifulsoup4`
* `trafilatura`
* `markdownify`
* `unstructured`

## **Text cleaning**

* `nltk`
* `spacy`
* `rapidfuzz`
* `cleantext`

---

# **8. Local Model Hosting & Acceleration**

## **Serving**

* `vllm` (BEST performance; supports OpenAI API compatibility)
* `text-generation-inference`
* `fastapi`
* `uvicorn`

## **Quantization / optimization**

* `bitsandbytes`
* `gguf` loaders (llama.cpp ecosystem)
* `optimum`
* `accelerate`
* `torch.compile`, `torch.cuda.amp`

---

# **9. Fine-Tuning (SFT, LoRA, QLoRA)**

## **Training Frameworks**

* `transformers`
* `peft` (QLoRA / LoRA)
* `accelerate`
* `trl` (RLHF, PPO, DPO)
* `deepspeed`
* `lightning` (PyTorch Lightning)

## **Datasets and tokenizers**

* `datasets`
* `tiktoken`
* `sentencepiece`
* `tokenizers`

---

# **10. Orchestration & Pipelines**

## **Workflow orchestration**

* `langgraph`
* `deepagents`
* `prefect`
* `airflow`
* `dagster`

## **Memory**

* `langchain.memory`
* vector-store memory
* filesystem memories

---

# **11. Speech, Vision, Multimodal**

## **Speech**

* `whisper`
* `pydub`
* `soundfile`
* Azure Speech SDK

## **Vision**

* `opencv-python`
* `pillow`
* `transformers` (CLIP, Vision models)
* `ultralytics` (YOLO)

## **Multimodal**

* GPT-4o / GPT-4.1 via `openai`
* Gemini Vision via `google-generativeai`
* LLaVA, MiniCPM-V, Florence-2 via `transformers`

---

# **12. UI for LLM apps**

* `gradio`
* `streamlit`
* `fastapi`
* `streamlit-webrtc` (multimodal)
* `chainlit`

---

# **13. Full-stack commercial / managed platforms (Python SDKs)**

(If you want robust hosted infra)

* **Bedrock** → `boto3`
* **Azure AI Foundry** → `azure.ai.ml`, `openai` API
* **Google Vertex AI** → `google-cloud-aiplatform`
* **Cohere Platform** → `cohere`
* **Mistral Platform** → `mistralai`

---

# **14. Summary Map**

```
         ┌──── Model Access (openai, transformers, vllm)
         │
         ├──── RAG (faiss, chroma, llamaindex, haystack)
         │
         ├──── Agents & Workflows (langchain, langgraph, deepagents)
         │
         ├──── Prompting & Guardrails (guidance, outlines, guardrails)
LLM Dev ─┤
Stack    │
         ├──── Evaluation (ragas, deepeval, trulens)
         │
         ├──── Finetuning (transformers, peft, trl, accelerate)
         │
         ├──── Data tooling (unstructured, pypdf, bs4)
         │
         └──── Serving (vllm, TGI, fastapi, uvicorn)
```

This is the **official modern map** of Python LLM tooling.

---

If you want, I can produce:

* A **recommended stack for your AI-Trader project**
* A **stack for your Azure migration assistant**
* A **stack for your multi-hop financial RAG system**
* A **flowchart diagram of all components**
