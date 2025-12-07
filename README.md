# 🚀 DevAgent AI — Intelligent Developer Automation Suite  
### *AI-Powered Test Generation • Debugging • Code Review • Log Analysis • Refactoring*

---

## 📌 Table of Contents  
- [🌟 Overview](#-overview)  
- [❗ Problem Statement](#-problem-statement)  
- [🤖 Why Agents? Why Kiro?](#-why-agents-why-kiro)  
- [🎯 Key Features](#-key-features)  
  - [🧪 Automated Test Generation](#-1-automated-test-generation)
  - [🐛 Code Debugger](#-2-code-debugger)
  - [👁️ AI Code Review](#️-3-ai-code-review)
  - [⚡ Refactor Bot](#-4-refactor-bot)
  - [📋 Log Analyzer](#-5-log-analyzer)
  - [💾 Database Dashboard](#-6-built-in-database-dashboard)
- [🏗 Architecture](#-architecture)  
- [🧰 Tech Stack](#-tech-stack)  
- [🔄 System Workflow](#-system-workflow)  
- [📦 Installation & Setup](#-installation--setup)  
- [🔌 API Endpoints](#-api-endpoints)  
- [🖼 Screenshots](#-screenshots)  
- [🗄 Database Structure](#-database-structure)  
- [🧠 Use Cases](#-use-cases)  
- [🔮 Future Enhancements](#-future-enhancements)  
- [📜 License](#-license)

---

# 🌟 Overview
**DevAgent AI** is a full-stack, agentic automation assistant built for developers.  
It eliminates repetitive engineering tasks such as:

- writing test cases  
- debugging code  
- performing code reviews  
- refactoring legacy code  
- analyzing log patterns  

It functions as a **developer co-pilot**, providing insights, automation, and improvements in a single place.

---

# ❗ Problem Statement  
Developers waste **30–45%** of their time on:

- Writing repetitive test cases  
- Debugging trivial errors  
- Searching for log anomalies  
- Conducting manual code reviews  
- Refactoring boilerplate or legacy code  

These tasks reduce productivity and slow down development, especially in fast-paced environments.

**DevAgent AI solves this by automating the entire workflow end-to-end.**

---

# 🤖 Why Agents? Why Kiro?

### Why Agents?
Agentic systems allow independent components to:

- Plan tasks  
- Execute workflows  
- Make decisions  
- Provide step-wise improvements  
- Work asynchronously  

DevAgent uses agentic behavior across modules:

- **TestAgent** → extracts structure, generates tests  
- **DebugAgent** → scans errors and suggests fixes  
- **ReviewAgent** → analyzes quality, performance, security  
- **RefactorAgent** → improves code structure  
- **LogAgent** → detects patterns & insights  

### Why Kiro IDE?
Kiro accelerated development via:

- Automated test generation specifications  
- Code scaffolding for backend  
- Workflow prototyping using Kiro templates  
- Improved iteration through AI-guided suggestions  

Kiro drastically reduced development time, enabling rapid prototyping of architecture & agents.

---

# 🎯 Key Features  

### 🧪 **1. Automated Test Generation**
- From pasted code  
- From Git Repositories  
- From ZIP uploads  
- From images (OCR-ready pipeline)  
- Multi-language (Python, Java, C#, JS, TS, Go, C/C++, Ruby, PHP)

---

### 🐛 **2. Code Debugger**
- Detects errors (syntax, divisions, null-reference, index issues)  
- Analyses error messages  
- Suggests AI-generated fixes  
- Produces explanations for each issue  

---

### 👁️ **3. AI Code Review**
- Quality score (0–100)  
- Security risk detection  
- Performance analysis  
- Readability improvements  
- Best-practice recommendations  
- Multi-language support  

---

### ⚡ **4. Refactor Bot**
- Modernization  
- Readability improvements  
- Python optimizations  
- Java enhancements  
- JavaScript optimizations  

---

### 📋 **5. Log Analyzer**
- Error pattern detection  
- Insights for performance issues  
- Breakdown of warnings, errors, and info logs  

---

### 💾 **6. Built-in Database Dashboard**
- Tracks every operation  
- Stores input/output snapshots  
- Maintains stats across all tools  
- SQLite based (serverless)

---

# 🏗 Architecture  

```
DevAgent/
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── jobs.py
│   │   ├── worker.py
│   │   └── utils.py
├── frontend/
│   ├── streamlit_app.py
├── data/
│   └── test_sight.db
└── docker-compose.yml
```

---

# 🧰 Tech Stack  

### **Frontend**
- Streamlit  
- Custom CSS  
- Sessions, caching, live metrics  

### **Backend**
- FastAPI  
- Pydantic  
- Async operations  
- CORS enabled  

### **Database**
- SQLite3  

### **Execution Tools**
- Pytest  
- Git CLI  

---

# 🔄 System Workflow

```
User Input →
    Streamlit UI →
        FastAPI Endpoint →
            Agent Module →
                Execution →
                    DB Logging →
                        Dashboard Display
```

---

# 📦 Installation & Setup  

## Backend Setup
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Frontend Setup
```bash
cd frontend
pip install -r requirements.txt
streamlit run streamlit_app.py
```

---

# 🔌 API Endpoints  

### **Test Generation**
```
POST /generate-tests
POST /jobs
GET  /jobs/{job_id}
```

### **Debugging**
```
POST /debug
```

### **Code Review**
```
POST /review
```

### **Refactoring**
```
POST /refactor
```

### **Log Analysis**
```
POST /analyze-logs
```

### **Activity Logs**
```
GET /activity-logs
DELETE /activity-logs
```

---

# 🖼 Screenshots  
(Add your screenshots here)

---

# 🗄 Database Structure  

### **activity_logs**
| Column | Type  | Description |
|--------|-------|-------------|
| id     | int   | PK          |
| activity_type | text | test/debug/review/etc. |
| input_data | text | input snippet |
| output_data | text | output summary |
| created_at | text | timestamp |

### **jobs**
| Column | Type  | Description |
|--------|-------|-------------|
| id     | int   | PK          |
| repo_url | text | Repository URL |
| status | text | queued/done/failed |
| created_at | text | timestamp |
| language | text | Programming language |

### **runs**
| Column | Type  | Description |
|--------|-------|-------------|
| id     | int   | PK          |
| job_id | int   | FK to jobs |
| tests_total | int | Total tests |
| tests_failed | int | Failed tests |
| coverage | real | Code coverage % |

---

# 🧪 Testing Guide  

## Quick Test
1. **Start Backend**: `cd backend && python -m uvicorn app.main:app --reload`
2. **Start Frontend**: `cd frontend && streamlit run streamlit_app.py`
3. **Test Each Feature**:
   - Go to **Debugger** → Paste code → Analyze
   - Go to **Code Review** → Paste code → Review
   - Go to **Dashboard** → See updated metrics

## Detailed Testing
See [TESTING_GUIDE.md](TESTING_GUIDE.md) for comprehensive test cases.

---

# 🧠 Use Cases  

- QA automation  
- Developer debugging  
- Secure code review  
- Log forensics  
- Legacy code modernization  

---

# 🔮 Future Enhancements  

- Advanced LLM-based agents  
- WebSockets streaming  
- JWT Authentication  
- Distributed job queue  
- PostgreSQL migration  

---

# 📜 License  
MIT License
