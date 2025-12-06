# Agent Discovery & Interview System# Agent Discovery Interview System# Agent Discovery & Interview System

This pipeline uses BM25 semantic search to find the top k agent cards that match a prompt. It then uses an interview agent to form questions and evaluate the responses of each candidate. Candidate agents are accessed through the URL endpoint in their agent cards.## Project StructureThis pipeline uses BM25 semantic search to find the top k agent cards that match a prompt. It then uses an interview agent to form questions and evaluate the responses of each candidate. Candidate agents are accessed through the URL endpoint in their agent cards.

## Features````## Features

- 🔍 **BM25 Search**: Semantic search to find best matching agentsagent-discovery-interview/

- 🤖 **Real AI Agents**: 8 specialized AI-powered agents using OpenAI GPT-4

- 💬 **Interview System**: Automated agent evaluation through Q&A├── python/ # Python backend - Agent discovery & interview- 🔍 **BM25 Search**: Semantic search to find best matching agents

- 📊 **Benchmarking**: Comprehensive benchmark suite for agent performance

│ ├── agent_bm25s.py # BM25 search implementation- 🤖 **Real AI Agents**: 8 specialized AI-powered agents using OpenAI GPT-4

## Project Structure

│ ├── interview.py # Interview and evaluation logic- 💬 **Interview System**: Automated agent evaluation through Q&A

`````

agent-discovery-interview/│   ├── main.py                     # Main discovery pipeline- 📊 **Benchmarking**: Comprehensive benchmark suite for agent performance

├── discovery-system/              # Python backend - Agent discovery & interview

│   ├── agent_bm25s.py            # BM25 search implementation│   ├── run_benchmark.py            # Benchmark runner

│   ├── interview.py              # Interview and evaluation logic

│   ├── main.py                   # Main discovery pipeline│   ├── requirements.txt            # Python dependencies## Quick Start

│   ├── run_all_queries.py        # Run all benchmark queries

│   ├── requirements.txt          # Python dependencies│   ├── agents.json                 # Agent configurations (external)

│   ├── agentList.json            # Agent configurations

│   ├── queryList.json            # Test queries│   ├── software_agents.json        # Local agent configurations### 1. Install Dependencies

│   └── benchmark_results.json    # Benchmark output results

││   ├── benchmark_queries.json      # Benchmark test queries

├── start-agents/                  # TypeScript - Real AI agent servers

│   ├── real_software_a2a_agent.ts # AI agent server implementation│   └── benchmark_results.json      # Benchmark output results```bash

│   ├── start_real_agents.ps1     # Start all 8 agents (Windows)

│   ├── start_real_agents.sh      # Start all 8 agents (Linux/Mac)│# Python dependencies

│   ├── package.json              # Node.js dependencies

│   └── tsconfig.json             # TypeScript configuration├── typescript/                      # TypeScript - Real AI agent serverspip install -r requirements.txt

│

├── .env                          # Environment variables (API keys)│   ├── real_software_a2a_agent.ts  # AI agent server implementation

├── .env.example                  # Environment variable template

├── README.md                     # This file│   ├── start_real_agents.ps1       # Start all 8 agents# Node.js dependencies (for agents)

└── FIXES_APPLIED.md              # Documentation of fixes

```│   ├── package.json                # Node.js dependenciesnpm install



## Quick Start│   ├── tsconfig.json               # TypeScript configuration```



### 1. Install Dependencies│   └── node_modules/               # Node dependencies



**Python dependencies:**│### 2. Configure Environment

```bash

cd discovery-system├── start_agents.ps1                # Quick start: Launch AI agents

pip install -r requirements.txt

```├── run_main.ps1                    # Quick start: Run discovery systemCopy `.env.example` to `.env` and add your OpenAI API key:



**Node.js dependencies (for agents):**├── run_benchmark.ps1               # Quick start: Run full benchmark

```bash

cd start-agents├── README.md                       # This file```bash

npm install

```├── .gitignore                      # Git ignore rulesOPENAI_API_KEY=your-api-key-here



### 2. Configure Environment└── .env.example                    # Environment variable template```



Copy `.env.example` to `.env` and add your OpenAI API key:````



```bash### 3. Start Real AI Agents

OPENAI_API_KEY=your-api-key-here

```## Quick Start



### 3. Start Real AI Agents```powershell



**Windows (PowerShell):**### 1. Install Dependencies.\start_real_agents.ps1

```powershell

cd start-agents```

.\start_real_agents.ps1

```**Python:**



**Linux/Mac (Bash):**```powershellThis starts 8 specialized AI agents on ports 12001-12008.

```bash

cd start-agentscd python

chmod +x start_real_agents.sh

./start_real_agents.shpip install -r requirements.txt### 4. Run Discovery & Interview

`````

`````

This starts 8 specialized AI agents on ports 12001-12008.

````bash

### 4. Run Discovery & Interview

**TypeScript/Node.js:**# Run with default agents

**Run single query demo:**

```bash```powershellpython main.py

cd discovery-system

python main.pycd typescript

`````

npm install# Run benchmarks

**Run full benchmark (all 24 queries):**

`bash`python run_benchmark.py

cd discovery-system

python run_all_queries.py````

`````

### 2. Configure Environment

## 8 Real AI Agents

## Project Structure

1. **Code Debugging Assistant** (Port 12001) - Debug errors across multiple languages

2. **API Design Advisor** (Port 12002) - REST, GraphQL, gRPC designCopy `.env.example` to `.env` and add your OpenAI API key:

3. **Performance Diagnostics Engineer** (Port 12003) - Performance issues, bottlenecks

4. **Frontend UX Refiner** (Port 12004) - React, Vue, accessibility````

5. **DevOps CI/CD Orchestrator** (Port 12005) - Docker, Kubernetes, cloud

6. **Secure Code Auditor** (Port 12006) - Security, OWASP, vulnerabilitiesOPENAI_API_KEY=your-api-key-here├── agent_bm25s.py              # BM25 search implementation

7. **Test Automation Engineer** (Port 12007) - Unit tests, TDD, automation

8. **Software Architecture Consultant** (Port 12008) - System design, patterns```├── interview.py                # Interview and evaluation logic



## Current Performance├── main.py                     # Main discovery pipeline



Based on 24-query benchmark:### 3. Run the System├── run_benchmark.py            # Benchmark runner

- **Top-1 Accuracy**: 70.8% (17/24 queries had correct agent ranked first)

- **Top-3 Recall**: 95.8% (23/24 queries had correct agent in top-3)├── real_software_a2a_agent.ts  # Real AI agent server



## How It Works**Start AI Agents** (from root):├── start_real_agents.ps1       # Start all 8 AI agents



1. **BM25 Search**: User query is tokenized and searched against agent prompts using BM25 algorithm```powershell├── software_agents.json        # Agent configurations

2. **Candidate Selection**: Top 3 agents are selected based on relevance scores

3. **Question Generation**: An interviewer AI generates a technical question based on the task.\start_agents.ps1└── agents.json                 # Alternative agent set

4. **Agent Response**: Each candidate agent receives the question and provides a detailed answer

5. **Evaluation**: A judge AI evaluates each answer and assigns a score (1-10)````

6. **Results**: All interviews are saved with rankings, questions, answers, and evaluations

**Run Discovery System** (from root):## 8 Real AI Agents

## Documentation

````powershell

- `FIXES_APPLIED.md` - Documentation of all code fixes and improvements

- `REAL_AI_AGENTS_SETUP.md` - Detailed agent setup guide (if exists).\run_main.ps11. **Code Debugging Assistant** (Port 12001) - Debug errors across multiple languages

- `BENCHMARK_RESULTS.md` - Benchmark analysis and results (if exists)

```2. **API Design Advisor** (Port 12002) - REST, GraphQL, gRPC design

## Output Files

3. **Backend Database Optimizer** (Port 12003) - SQL optimization, schema design

- `demo_output_<timestamp>.txt` - Single query demo results

- `all_queries_output_<timestamp>.txt` - Full benchmark human-readable output**Run Full Benchmark** (from root):4. **Frontend UX Refiner** (Port 12004) - React, Vue, accessibility

- `query_results_<timestamp>.json` - Full benchmark structured JSON results

```powershell5. **DevOps CI/CD Orchestrator** (Port 12005) - Docker, Kubernetes, cloud

## Stopping Agents

.\run_benchmark.ps16. **Secure Code Auditor** (Port 12006) - Security, OWASP, vulnerabilities

**Windows:**

- Close the PowerShell windows that were opened for each agent```7. **Test Automation Engineer** (Port 12007) - Unit tests, TDD, automation



**Linux/Mac:**8. **Software Architecture Consultant** (Port 12008) - System design, patterns

```bash

pkill -f 'ts-node real_software_a2a_agent.ts'## Features

`````

## Documentation

## License

- 🔍 **BM25 Search**: Semantic search to find best matching agents

MIT

- 🤖 **8 Real AI Agents**: Specialized AI-powered agents using OpenAI GPT-4- `REAL_AI_AGENTS_SETUP.md` - Detailed agent setup guide

- 💬 **Interview System**: Automated agent evaluation through Q&A- `BENCHMARK_RESULTS.md` - Benchmark analysis and results

- 📊 **Benchmarking**: Comprehensive benchmark suite for agent performance- `SETUP_COMPLETE.md` - Initial setup documentation

## 8 Real AI Agents

1. **Code Debugging Assistant** (Port 12001) - Debug errors across multiple languages
2. **API Design Advisor** (Port 12002) - REST, GraphQL, gRPC design
3. **Backend Database Optimizer** (Port 12003) - SQL optimization, schema design
4. **Frontend UX Refiner** (Port 12004) - React, Vue, accessibility
5. **DevOps CI/CD Orchestrator** (Port 12005) - Docker, Kubernetes, cloud
6. **Secure Code Auditor** (Port 12006) - Security, OWASP, vulnerabilities
7. **Test Automation Engineer** (Port 12007) - Unit tests, TDD, automation
8. **Software Architecture Consultant** (Port 12008) - System design, patterns

## Running from Within Folders

**From python/ directory:**

```powershell
cd python
python main.py           # Run discovery
python run_benchmark.py  # Run benchmark
```

**From typescript/ directory:**

```powershell
cd typescript
.\start_real_agents.ps1  # Start agents
```

## Documentation

- `EVALUATION_METRICS.md` - Detailed metrics explanation
- `REAL_AI_AGENTS_SETUP.md` - Agent setup guide
- `BENCHMARK_RESULTS.md` - Benchmark analysis

## Current Performance

- **Accuracy**: 68.8% (11/16 queries)
- **Precision@1**: 11.8% (correct agent ranked first)
- **Recall@3**: 68.8% (correct agent in top-3)
- **F1 Score**: 20.2%
