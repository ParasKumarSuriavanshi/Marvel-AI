# 🤖 Marvel AI

> **A local-first, modular AI personal assistant for desktop automation, web intelligence, memory, and natural voice interaction.**

Marvel AI is a personal AI assistant designed to behave like a **local, customizable, Jarvis-style assistant** while remaining modular enough to evolve into a larger AI agent platform.

The project combines **Python, LangGraph, LangChain, local LLMs, structured command routing, web automation, web scraping, information retrieval, vector databases, persistent memory, and desktop automation** into a single agentic architecture.

The long-term goal is to build an assistant that can understand natural language, decide whether a request can be executed directly or requires an AI agent, interact with applications and websites, retrieve current information from the web, remember useful user-specific information, and provide concise personalized responses.

---

## ✨ Project Highlights

Marvel AI is being developed around several core principles:

* 🧠 **Local-first AI**
* 🎯 **Deterministic command execution where possible**
* 🌐 **Real-time web search and retrieval**
* 🔎 **Web scraping and structured content extraction**
* 🗂️ **Persistent user memory**
* 🧩 **Modular agent architecture**
* 🛠️ **Tool-based execution**
* 🗣️ **Voice interaction**
* ⚡ **Fast-path commands**
* 🔐 **User-specific memory isolation**
* 📝 **Structured outputs**
* 📊 **Extensive logging**
* 🚫 **Reduced hallucination through retrieval and deterministic execution**
* 🔌 **Designed for future expansion to other devices**

---

# 🎯 Vision

The goal of Marvel AI is not simply to create another chatbot.

The goal is to build an **AI operating layer** capable of interacting with the user's digital environment.

A typical request could eventually look like:

```text
Hey Marvel, search for the latest information about LangGraph,
summarize the important points, and save the useful information.
```

Marvel AI should be able to:

```text
Voice Input
     ↓
Speech Recognition
     ↓
Command / Intent Detection
     ↓
Command Routing
     ↓
┌─────────────────────────────┐
│ Direct Command              │
│ OR                          │
│ AI Agent / Tool Execution   │
└─────────────────────────────┘
     ↓
Tools / Web / Memory / Apps
     ↓
Result Processing
     ↓
Response Generation
     ↓
Personalized Response
     ↓
Voice / Text Output
```

The architecture is intentionally designed so that simple operations do **not** require an LLM unnecessarily.

For example:

```text
Open Chrome
```

should not require a complex reasoning pipeline.

Whereas:

```text
Find the latest information about LangGraph
and explain the important changes.
```

requires web search, retrieval, processing, and AI reasoning.

---

# 🏗️ Current Architecture

The current Marvel AI architecture is evolving toward the following structure:

```text
                         ┌────────────────────┐
                         │      USER          │
                         └─────────┬──────────┘
                                   │
                         Voice / Text Input
                                   │
                                   ▼
                         ┌────────────────────┐
                         │ Speech Recognition │
                         │ / Input Processor  │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │    Normalizer      │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │  Command Parser    │
                         └─────────┬──────────┘
                                   │
                                   ▼
                         ┌────────────────────┐
                         │   Command Router   │
                         └───────┬─────┬──────┘
                                 │     │
                     Direct      │     │      AI / Complex
                     Command     │     │      Request
                                 │     │
                                 ▼     ▼
                         ┌──────────┐ ┌──────────────┐
                         │ Fast Path│ │ Main Agent   │
                         └────┬─────┘ └──────┬───────┘
                              │              │
                              │              ▼
                              │      ┌───────────────┐
                              │      │ Tool System   │
                              │      └───────┬───────┘
                              │              │
                              │       ┌──────┼─────────┐
                              │       │      │         │
                              ▼       ▼      ▼         ▼
                         Desktop    Web    Memory    System
                         Tools      Tools  Tools     Tools
                              │       │      │         │
                              └───────┴──────┴─────────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │ Draft Agent   │
                              └───────┬───────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │ Personality / │
                              │ Response Agent│
                              └───────┬───────┘
                                      │
                                      ▼
                              ┌───────────────┐
                              │ Final Response │
                              └───────────────┘
```

---

# 🚀 Current Development Status

Marvel AI is being developed incrementally.

## ✅ Completed / Working

### Core Architecture

* [x] Python-based assistant architecture
* [x] Modular project structure
* [x] LangGraph-based workflow architecture
* [x] Local LLM integration
* [x] Structured command processing
* [x] Command normalization
* [x] Rule-based command parsing
* [x] Basic command routing
* [x] Direct command execution architecture
* [x] Logging architecture

### Memory System

* [x] User-specific memory architecture
* [x] Profile memory
* [x] Episodic memory
* [x] Semantic memory architecture
* [x] SQLite-based episodic memory
* [x] Vector-based semantic retrieval
* [x] Memory IDs for persistent records
* [x] Memory CRUD architecture
* [x] Structured memory operations
* [x] User isolation through `user_id`

### Web Intelligence

* [x] Browser automation
* [x] Playwright integration
* [x] Web search workflow
* [x] Website navigation
* [x] Link extraction
* [x] Web page scraping
* [x] Basic content extraction
* [x] Retrieved content processing
* [x] Basic web retrieval pipeline
* [x] Basic search commands

### Direct Commands

Basic deterministic commands are supported through a rule-based approach.

Examples:

```text
open chrome
open whatsapp
open calculator
open netflix

close chrome

set volume to 50

search what is langgraph
```

---

# 🧠 Why a Hybrid AI Architecture?

One of the important architectural decisions in Marvel AI is that **not every request should be handled by an LLM**.

A purely LLM-driven assistant introduces unnecessary latency, cost, and unpredictability for deterministic operations.

Instead, Marvel AI uses a hybrid approach.

## Example

### Request

```text
Open Chrome
```

The system can process it as:

```text
Input
 ↓
Normalize
 ↓
Match command rule
 ↓
OPEN_APPLICATION
 ↓
Chrome
 ↓
Execute
```

No LLM reasoning is required.

---

### Complex Request

```text
Explain how LangGraph works and search the web
for the latest information.
```

This requires:

```text
Input
 ↓
Normalization
 ↓
Command analysis
 ↓
AI routing
 ↓
Web tool
 ↓
Search
 ↓
Scraping
 ↓
Content extraction
 ↓
Retrieval
 ↓
LLM reasoning
 ↓
Response
```

This approach provides a balance between:

* Speed
* Reliability
* Cost
* Deterministic execution
* AI reasoning
* Extensibility

---

# ⚡ Command Processing Pipeline

Marvel AI uses multiple stages before executing commands.

```text
Raw User Input
      │
      ▼
┌──────────────┐
│ Normalization│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Command Split│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Command Parser│
└──────┬───────┘
       │
       ▼
┌──────────────┐
│ Command Router│
└──────┬───────┘
       │
       ├───────────────┐
       ▼               ▼
 Direct             AI Agent
 Command            / Tools
       │               │
       └───────┬───────┘
               ▼
           Execution
```

---

# 🔎 Command Parser

The command parser converts natural language into structured commands.

For example:

```text
Open Chrome
```

can become:

```json
{
    "command": "OPEN_APPLICATION",
    "arguments": {
        "application": "chrome"
    }
}
```

Another example:

```text
Set volume to 50
```

becomes:

```json
{
    "command": "SET_VOLUME",
    "arguments": {
        "volume": 50
    }
}
```

A web request:

```text
Search what is LangGraph
```

can become:

```json
{
    "command": "WEB_SEARCH",
    "arguments": {
        "query": "what is langgraph"
    }
}
```

This structured representation allows the execution layer to remain independent from the original natural-language input.

---

# 🌐 Web Intelligence System

One of the major parts of Marvel AI is its web intelligence pipeline.

The objective is to allow the assistant to retrieve **current information from websites instead of relying entirely on the knowledge stored inside the LLM**.

## Web Retrieval Flow

```text
User Query
    │
    ▼
Search Query
    │
    ▼
Browser / Search Engine
    │
    ▼
Search Results
    │
    ▼
Relevant URLs
    │
    ▼
Playwright
    │
    ▼
Website Navigation
    │
    ▼
Page Content Extraction
    │
    ▼
Content Cleaning
    │
    ▼
Structured Documents
    │
    ▼
Chunking
    │
    ▼
Embeddings
    │
    ▼
Vector Retrieval
    │
    ▼
Relevant Context
    │
    ▼
LLM
    │
    ▼
Final Answer
```

---

# 🕷️ Web Scraping

Playwright is used to interact with websites programmatically.

The system can:

* Open websites
* Navigate between pages
* Extract links
* Retrieve page content
* Inspect HTML elements
* Extract text
* Identify relevant pages
* Process dynamic websites

Example:

```python
links = await page.locator("a").evaluate_all(
    "elements => elements.map(el => el.href)"
)
```

The extracted links can then be filtered and processed before being passed into the retrieval pipeline.

---

# 📄 Web Content Extraction

Raw HTML is not directly useful to the LLM.

Marvel AI therefore aims to transform:

```text
HTML
 ↓
DOM
 ↓
Visible content
 ↓
Clean text
 ↓
Structured document
 ↓
Chunks
 ↓
Embeddings
```

A structured document can conceptually contain:

```json
{
    "url": "https://example.com",
    "title": "Example Page",
    "content": "Extracted page content...",
    "metadata": {
        "source": "web",
        "domain": "example.com"
    }
}
```

This makes web content easier to retrieve and process.

---

# 🔍 Retrieval-Augmented Generation

Marvel AI uses retrieval to provide relevant external information to the LLM.

The conceptual pipeline is:

```text
Query
  │
  ▼
Embedding
  │
  ▼
Vector Search
  │
  ▼
Relevant Documents
  │
  ▼
Context Construction
  │
  ▼
LLM
  │
  ▼
Answer
```

This allows the assistant to separate:

### Knowledge

Stored model knowledge.

### Retrieved information

Information dynamically obtained from external sources.

### User memory

Information specifically stored for the user.

This separation is important for building a controllable assistant.

---

# 🧠 Memory Architecture

Marvel AI includes a persistent memory system designed around different types of information.

```text
                 MEMORY SYSTEM
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
       Profile     Episodic    Semantic
       Memory      Memory      Memory
          │           │           │
          ▼           ▼           ▼
        SQLite      SQLite      Vector DB
```

## Profile Memory

Stores relatively stable user information.

Example:

```text
operating_system = Arch Linux
response_style = concise
```

---

## Episodic Memory

Stores events or experiences.

Example:

```text
Event:
User completed web retrieval implementation.

Context:
Marvel AI development.

Summary:
The web scraping and retrieval pipeline was successfully implemented.

Importance:
High
```

---

## Semantic Memory

Stores knowledge and relationships.

Example:

```text
Subject: Marvel AI
Predicate: uses
Object: LangGraph
```

Semantic information can be embedded and retrieved through vector search.

---

# 👤 User Isolation

Marvel AI is designed to support multiple users without mixing their memories.

A memory operation contains a user identifier:

```json
{
    "user_id": "001",
    "memory_type": "profile",
    "action": "create",
    "data": {
        "field": "response_style",
        "value": "concise"
    }
}
```

The architecture is designed so that each user's memories can be independently retrieved and managed.

---

# 🤖 Local LLM Architecture

Marvel AI is designed around local models wherever practical.

The current development stack has included:

* Ollama
* Qwen models
* Nomic embeddings
* LangChain
* LangGraph

Example architecture:

```text
Marvel AI
    │
    ▼
LangChain / LangGraph
    │
    ▼
Ollama
    │
    ├── Chat Model
    │
    └── Embedding Model
```

The use of local models provides several advantages:

* Reduced dependence on cloud APIs
* Better privacy
* Offline capability for supported functionality
* No per-request API cost
* Greater control over model selection
* Easier experimentation with different models

---

# 🧩 Agent Architecture

The planned agent architecture separates responsibilities instead of placing everything inside one enormous prompt.

## Main Agent / Orchestrator

Responsible for:

* Understanding the overall request
* Selecting the appropriate workflow
* Calling tools
* Managing execution
* Coordinating other agents

---

## Draft Response Agent

Responsible for producing a technically complete response using:

* User request
* Conversation context
* Tool results
* Retrieved information
* Memory

---

## Response / Personality Agent

Responsible for transforming the draft into Marvel AI's final response style.

This separation allows reasoning and presentation to remain independent.

Conceptually:

```text
User
 ↓
Main Agent
 ↓
Tools / Retrieval / Memory
 ↓
Draft Response
 ↓
Personality Agent
 ↓
Final Response
```

---


# 🖥️ Application Automation

Marvel AI is intended to control installed applications using deterministic tools.

Example:

```text
User:
Open Chrome
```

Flow:

```text
User Input
    ↓
Command Parser
    ↓
OPEN_APPLICATION
    ↓
Application Resolver
    ↓
Chrome
    ↓
Execute
```

Application aliases can be maintained separately.

Example:

```json
{
    "chrome": "google-chrome",
    "browser": "google-chrome",
    "whatsapp": "whatsapp",
    "calculator": "gnome-calculator"
}
```

This allows the command parser to remain independent from operating-system-specific application names.

---

# 🎙️ Voice Assistant

The long-term interface for Marvel AI is voice.

The intended interaction is:

```text
"Hey Marvel, open Chrome."
```

rather than:

```text
"Hey Marvel"

(wait)

"Open Chrome"
```

The assistant is designed around:

```text
Wake Word
    ↓
Speech Recognition
    ↓
Command Processing
    ↓
Execution
    ↓
Voice Response
```

The voice layer is intentionally separated from the core AI system so that text input can also be used during development and testing.

---

# ⚡ Fast-Path Commands

Fast-path commands are one of the key performance optimizations.

Instead of:

```text
User
 ↓
LLM
 ↓
Reasoning
 ↓
Tool selection
 ↓
Execution
```

a deterministic command can use:

```text
User
 ↓
Normalizer
 ↓
Parser
 ↓
Direct Tool
 ↓
Result
```

This reduces:

* Latency
* Token usage
* Unnecessary model calls
* Execution uncertainty

---

# 📝 Structured Outputs

Marvel AI uses structured representations whenever possible.

For example, instead of asking an LLM to return free-form text describing a memory operation, the memory layer can work with structured objects.

Conceptually:

```json
{
    "memory_required": true,
    "memories": [
        {
            "memory_type": "episodic",
            "action": "create",
            "data": {},
            "confidence": 0.95,
            "reason": "Important project milestone"
        }
    ]
}
```

Structured outputs make downstream processing more predictable.

---

# 🧪 Error Handling

A production-quality assistant needs to handle failures explicitly.

Potential failure points include:

```text
Speech Recognition
       ↓
Command Parsing
       ↓
Routing
       ↓
Tool Execution
       ↓
Web Search
       ↓
Page Loading
       ↓
Content Extraction
       ↓
Retrieval
       ↓
LLM Generation
```

Marvel AI is being designed so errors can be:

* Logged
* Classified
* Returned safely
* Retried where appropriate
* Presented to the user clearly

For example:

```text
Tool Error
    ↓
Error Handler
    ↓
Logging
    ↓
Retry / Fallback
    ↓
User Response
```

---

# 📊 Logging

Logging is an important part of the architecture.

Marvel AI is intended to record important system events such as:

```text
INPUT RECEIVED
      ↓
NORMALIZATION
      ↓
COMMAND PARSED
      ↓
ROUTE SELECTED
      ↓
TOOL CALLED
      ↓
TOOL RESULT
      ↓
AGENT RESPONSE
      ↓
FINAL RESPONSE
```

This makes debugging complex agent workflows significantly easier.

---

# 🗂️ Project Structure

The project is being organized into modular components.

A simplified representation:

```text
Marvel-AI/
│
├── agent/
│   ├── __init__.py
│   ├── Marvel_AI.py
│   └── user_id.py
│
├── database/
│   ├── json/
│   ├── sql/
│   └── vector/
│
├── direct_command/
│   ├── command_info/
│   │   ├── __init__.py
│   │   ├── application.py
│   │   └── rules.py
│   │
│   ├── __init__.py
│   ├── command_executor.py
│   ├── command_parser.py
│   ├── normalizer.py
│   └── workflow_command.py
│
├── graph/
│   ├── __init__.py
│   ├── fake_state.py
│   ├── route.py
│   ├── state.py
│   ├── update_range.py
│   └── workflow.py
│
├── memory/
│   ├── checkpoint.py
│   ├── episodic.py
│   ├── manager.py
│   ├── profile.py
│   └── semantic_json.py
│
├── model/
│   ├── __init__.py
│   └── llm.py
│
├── retrieve/
│   └── vectorStore/
│       ├── episodic_vt.py
│       └── semantic.py
│
├── web/
│   ├── browser_controller.py
│   └── content_extractor.py
│
├── .gitignore
├── log_info.log
├── main.py
└── README.md
```

> The exact directory structure may change as the architecture evolves.

---

# 🧰 Technology Stack

| Category           | Technology                            |
| ------------------ | ------------------------------------- |
| Language           | Python                                |
| Agent Framework    | LangGraph                             |
| LLM Framework      | LangChain                             |
| Local LLM Runtime  | Ollama                                |
| LLMs               | Qwen family                           |
| Embeddings         | Nomic Embed                           |
| Vector Search      | FAISS                                 |
| Database           | SQLite                                |
| Browser Automation | Playwright                            |
| Web Retrieval      | Custom search + scraping pipeline     |
| Speech Recognition | Local speech recognition pipeline     |
| Version Control    | Git                                   |
| Operating System   | Linux / Arch Linux during development |

---

# 🔬 Engineering Principles

Marvel AI follows several engineering principles.

## 1. Deterministic Before Generative

If a request can be safely solved using deterministic logic, the system should avoid unnecessary LLM reasoning.

---

## 2. Modular Architecture

Components should be replaceable.

For example:

```text
Speech Recognition
```

should be replaceable without rewriting:

```text
Command Router
```

Similarly:

```text
LLM
```

should be replaceable without rewriting:

```text
Memory Database
```

---

## 3. Structured Data Between Components

Agents and tools should communicate using structured representations wherever practical.

---

## 4. Retrieval Before Guessing

When current external information is required, Marvel AI should retrieve information instead of expecting the model to know it.

---

## 5. Local-First

Where practical, functionality should work locally without depending on paid cloud APIs.

---

## 6. Observable Execution

Important operations should be logged so the system can be debugged.

---

## 7. User-Specific Memory

Memory should be isolated by user rather than treated as one global knowledge store.

---

# 🔐 Privacy Philosophy

Marvel AI is designed with a local-first approach.

The architecture aims to keep:

* User memory
* Local model inference
* Personal assistant data
* Application interaction

under the user's control wherever technically possible.

External web access is used when the assistant needs information from the internet.

---

# 💻 Installation

## Requirements

Recommended environment:

```text
Python 3.x
Git
Ollama
Playwright
SQLite
FAISS
LangChain
LangGraph
```

---

## Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd Marvel-AI
```

---

## Create a Virtual Environment

```bash
python -m venv .venv
```

Activate it:

### Linux

```bash
source .venv/bin/activate
```

### Windows

```powershell
.venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🦙 Ollama Setup

Install Ollama according to your operating system.

Then pull the required models.

Example:

```bash
ollama pull qwen3:8b
```

For embeddings:

```bash
ollama pull nomic-embed-text
```

Verify:

```bash
ollama list
```

The exact models may change as the project evolves.

---

# 🌐 Playwright Setup

After installing the Python package:

```bash
pip install playwright
```

install the required browser:

```bash
playwright install
```

For Linux environments, additional system dependencies may be required:

```bash
playwright install-deps
```

---

# ▶️ Running Marvel AI

Start the application using:

```bash
python main.py
```

During development, individual components can also be tested independently.

For example:

```bash
python command/command_parser.py
```

or through the project's test suite.

---

# 🧪 Example Commands

## Application Commands

```text
open chrome
```

```text
open whatsapp
```

```text
open calculator
```

```text
close chrome
```

---

## System Commands

```text
set volume to 50
```

Future examples:

```text
increase brightness
```

```text
decrease volume
```

---

## Web Search

```text
search what is langgraph
```

Expected conceptual flow:

```text
Query
 ↓
Search
 ↓
Search Results
 ↓
Relevant URLs
 ↓
Playwright
 ↓
Scraping
 ↓
Content Extraction
 ↓
Retrieval
 ↓
LLM
 ↓
Answer
```

---

# 🔥 More Complex Example

Input:

```text
Open Chrome and search for Marvel AI
```

The assistant should eventually be capable of decomposing the request into:

```text
1. OPEN_APPLICATION
   application = chrome

2. WEB_SEARCH
   query = Marvel AI
```

Then:

```text
Command 1
    ↓
Open Chrome

Command 2
    ↓
Search Web
```

This illustrates why command decomposition and routing are important parts of the architecture.

---

# 📈 Development Roadmap

## Phase 1 — Foundation

* [x] Project architecture
* [x] Local LLM integration
* [x] LangGraph workflow
* [x] Basic command system
* [x] Memory architecture

---

## Phase 2 — Intelligent Routing

* [x] Command normalization
* [x] Rule-based command parser
* [x] Basic command routing
* [x] Direct command execution
* [x] Initial tool architecture
* [ ] Advanced command decomposition
* [ ] Better fallback routing
* [ ] Complex multi-command execution

---

## Phase 3 — Web Intelligence

* [x] Playwright integration
* [x] Web navigation
* [x] Link extraction
* [x] Basic web scraping
* [x] Basic content extraction
* [x] Basic retrieval
* [ ] Advanced content cleaning
* [ ] Better relevance filtering
* [ ] Search-result ranking
* [ ] Improved chunking
* [ ] Retrieval evaluation
* [ ] Source-aware responses
* [ ] Temporary web knowledge lifecycle

---

## Phase 4 — Advanced Agent System

* [ ] Main orchestrator
* [ ] Draft response agent
* [ ] Personality response agent
* [ ] Tool selection
* [ ] Tool validation
* [ ] Agent error recovery
* [ ] Multi-step tool execution
* [ ] Agent state management

---

## Phase 5 — Desktop Automation

* [ ] Application control
* [ ] System control
* [ ] File operations
* [ ] Browser control
* [ ] Media control
* [ ] Window management
* [ ] System monitoring

---

## Phase 6 — Voice

* [ ] Reliable wake-word detection
* [ ] Single-sentence wake + command
* [ ] Local speech recognition
* [ ] Custom assistant voice
* [ ] Continuous interaction
* [ ] Voice interruption handling

---

## Phase 7 — Personalization

* [x] Profile memory architecture
* [x] Episodic memory architecture
* [x] Semantic memory architecture
* [ ] Automatic memory extraction improvements
* [ ] Memory relevance ranking
* [ ] Memory conflict resolution
* [ ] Better personalization
* [ ] User preference learning

---

## Phase 8 — Multi-Device Assistant

Long-term goal:

```text
                 Marvel AI
                    │
          ┌─────────┼─────────┐
          │         │         │
        Laptop      PC      Phone
          │         │         │
          └─────────┼─────────┘
                    │
                 Wi-Fi
                    │
          ┌─────────┼─────────┐
          │         │         │
        Smart    Home      Other
       Devices  Appliances Devices
```

The objective is to eventually allow Marvel AI to operate as a distributed personal assistant rather than being restricted to a single machine.

---

# 🧠 Why This Project Is Technically Interesting

Marvel AI combines multiple areas of modern software and AI engineering:

### Artificial Intelligence

* LLMs
* Prompt engineering
* Structured generation
* Agent workflows
* RAG
* Embeddings
* Semantic retrieval

### Software Engineering

* Modular architecture
* State management
* Error handling
* Logging
* Testing
* Database design
* API/tool abstraction

### AI Agents

* Orchestration
* Tool calling
* Routing
* Multi-step execution
* Memory
* Agent state

### Web Engineering

* Browser automation
* Web scraping
* DOM extraction
* Content processing
* Search
* Retrieval

### Systems

* Application control
* Linux integration
* Local model inference
* Hardware/system interaction

---

# 📊 Architecture Philosophy

Marvel AI is intentionally **not designed as one giant LLM prompt**.

Instead:

```text
                    ┌──────────────┐
                    │ User Input   │
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │ Deterministic│
                    │ Processing   │
                    └──────┬───────┘
                           │
                     Can execute?
                      /          \
                    YES           NO
                    │              │
                    ▼              ▼
                Direct Tool      AI Agent
                    │              │
                    │        ┌─────▼─────┐
                    │        │ Tool Use  │
                    │        └─────┬─────┘
                    │              │
                    └──────┬───────┘
                           ▼
                       Result
                           │
                           ▼
                    Final Response
```

This separation makes the system easier to:

* Debug
* Test
* Extend
* Optimize
* Monitor
* Maintain

---

# 🧪 Testing Strategy

Testing will eventually exist at multiple levels.

## Unit Tests

Test individual components:

```text
Normalizer
Parser
Router
Tools
Memory
Retriever
Extractor
```

---

## Integration Tests

Test workflows:

```text
Input
 ↓
Parser
 ↓
Router
 ↓
Tool
 ↓
Result
```

---

## Agent Tests

Test:

* Tool selection
* Structured output
* Retrieval
* Memory operations
* Failure handling

---

## End-to-End Tests

Example:

```text
User:
Search what is LangGraph
```

Expected:

```text
Speech/Text Input
 ↓
Command Processing
 ↓
Web Search
 ↓
Scraping
 ↓
Retrieval
 ↓
LLM
 ↓
Response
```

---

# 📝 Example End-to-End Web Query

Consider:

```text
Search what is LangGraph
```

Marvel AI can process the request approximately as:

```text
                    User Query
                        │
                        ▼
                "what is LangGraph"
                        │
                        ▼
                 Query Normalizer
                        │
                        ▼
                  Command Router
                        │
                        ▼
                    Web Tool
                        │
                        ▼
                 Search Engine
                        │
                        ▼
                  Search Results
                        │
                        ▼
                  Relevant URLs
                        │
                        ▼
                    Playwright
                        │
                        ▼
                  Page Extraction
                        │
                        ▼
                  Content Cleaner
                        │
                        ▼
                    Chunking
                        │
                        ▼
                   Embeddings
                        │
                        ▼
                 Vector Retrieval
                        │
                        ▼
                 Relevant Context
                        │
                        ▼
                       LLM
                        │
                        ▼
                 Draft Response
                        │
                        ▼
               Personality Layer
                        │
                        ▼
                  Final Answer
```

---

# 🏆 Project Goals

The long-term goals of Marvel AI are:

* Build a capable local personal assistant
* Minimize unnecessary cloud dependencies
* Combine deterministic automation with LLM reasoning
* Provide reliable web-grounded answers
* Maintain persistent user-specific memory
* Build a reusable agent/tool architecture
* Support voice interaction
* Control desktop applications
* Scale toward multi-device interaction

---

# 🔮 Future Possibilities

Potential future capabilities include:

```text
Calendar
Email
Files
Browser
Music
Smart Home
Phone
Laptop
Desktop
IoT
Personal Knowledge Base
Coding Assistant
Research Assistant
Automation
```

The goal is to provide a common AI interface across these systems.

---

# ⚠️ Current Limitations

Marvel AI is an active development project.

Current limitations include:

* Voice interaction is still being developed.
* Some application-control workflows are platform dependent.
* Web extraction quality varies between websites.
* Dynamic websites may require site-specific handling.
* Retrieval quality depends on search results and extracted content.
* Agent reliability is still being improved.
* Multi-step task execution is under development.
* The architecture and APIs may change as development continues.

---

# 🛡️ Design Goal: Reduce Hallucination

A major design objective is to reduce unsupported responses.

Marvel AI uses several mechanisms to accomplish this:

```text
Deterministic Commands
        +
Structured Outputs
        +
Tool Execution
        +
Web Retrieval
        +
Persistent Memory
        +
Source-Aware Context
        +
Logging
```

Instead of expecting the LLM to perform every operation internally, the architecture gives it access to external tools and verified intermediate results.

---

# 👨‍💻 Development Philosophy

Marvel AI is being built as a learning and engineering project focused on understanding how modern AI assistants actually work internally.

The project explores:

* How agents are orchestrated
* How LLMs interact with tools
* How memory systems can be designed
* How RAG pipelines work
* How web information can be retrieved
* How deterministic and probabilistic systems can coexist
* How local AI systems can be optimized
* How large AI systems can be broken into maintainable components

---

# 📚 What I Am Learning Through This Project

This project involves practical experience with:

```text
Python
LLMs
LangChain
LangGraph
Ollama
RAG
FAISS
Embeddings
SQLite
Playwright
Web Scraping
Browser Automation
Agent Architecture
Tool Calling
Memory Systems
Prompt Engineering
Structured Outputs
Git
Linux
System Automation
```

---

# 🚧 Status

> **Active Development**

Marvel AI is continuously evolving.

The current implementation has progressed from a basic voice-assistant concept toward a modular AI-agent architecture with:

```text
Command Processing
        +
Direct Execution
        +
Web Scraping
        +
Web Retrieval
        +
Memory
        +
Local LLMs
        +
Agent Orchestration
```

More advanced agent, automation, voice, and multi-device capabilities are planned.

---

# 🤝 Contributions

This is currently a personal development project, but ideas, discussions, bug reports, and technical suggestions are welcome.

If you find a problem:

1. Open an issue.
2. Explain the expected behavior.
3. Provide the actual behavior.
4. Include relevant logs or reproduction steps where possible.

---

# 📌 Future Documentation

Additional documentation will cover:

* Architecture
* Command parser
* Command router
* Agent workflows
* Memory architecture
* Web retrieval
* Playwright scraping
* Tool development
* Voice pipeline
* Configuration
* Testing
* Deployment

---

# ⭐ Project

**Marvel AI** is an ongoing attempt to build a modular, local-first AI assistant that combines:

> **AI reasoning + deterministic automation + web intelligence + memory + voice + tools**

The project is intentionally being developed incrementally, with each subsystem designed to be understandable, testable, and replaceable.

---

## 📬 Contact

For questions, collaboration, or discussion about the project, please use the contact information available on my GitHub profile.

---

<p align="center">

### 🤖 Marvel AI

**Building a personal AI assistant, one subsystem at a time.**

</p>
