# Financial Document Analyzer

## Project Overview
A comprehensive financial document analysis system that processes corporate reports, financial statements, and investment documents using AI-powered analysis agents. This version has been debugged and enhanced to provide reliable, evidence-based financial analysis.

## Setup and Usage

### 1. Install Required Libraries
```sh
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Create a `.env` file in the root of the project and add your NVIDIA API key:
```
NVIDIA_NIM_API_KEY="your_nvidia_api_key_here"
NVIDIA_BASE_URL="https://integrate.api.nvidia.com/v1"
```

### 3. Run the Application
```sh
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

### 4. Access the Web Interface
Open your browser and navigate to `http://localhost:8000`. You can upload a financial document (PDF) and enter a query to start the analysis.

## Live API Endpoint

You can access and test the API directly at the following link:

[saiphanidharreddy.onthewifi.com](https://saiphanidharreddy.onthewifi.com)

---

## Bugs Found and Fixed

This section details the bugs that were present in the original version of the project and the fixes that were implemented.

### 1. Core Logic and API (`main.py`)

- **Bug:** The application was missing several key agents and tasks, resulting in incomplete analysis.
- **Fix:** Imported and integrated all three agents (`financial_analyst`, `investment_advisor`, `risk_assessor`) and their corresponding tasks to create a complete analysis pipeline.

- **Bug:** The API response was unstructured and returned the raw output from the CrewAI kickoff.
- **Fix:** The `run_crew` function was updated to return a structured JSON object with clearly labeled results from each agent.

- **Bug:** The `file_path` of the uploaded document was not being passed to the analysis crew, preventing the agents from accessing the file.
- **Fix:** The `file_path` is now correctly passed to the `run_crew` function.

### 2. Agent Configuration (`agents.py`)

- **Bug:** The `llm` variable was undefined, causing the application to crash.
- **Fix:** Properly initialized the `ChatNVIDIA` model with the necessary API credentials and assigned it to the `llm` variable.

- **Bug:** The agent personas were unprofessional and encouraged fabricated, unreliable analysis.
- **Fix:** The agent backstories and goals were rewritten to be professional and evidence-based, instructing them to rely only on the provided document.

- **Bug:** The tool was referenced incorrectly, and a redundant `verifier` agent was included.
- **Fix:** Corrected the tool reference and removed the unnecessary `verifier` agent to streamline the crew.

### 3. Task Definitions (`task.py`)

- **Bug:** Task descriptions were vague and encouraged agents to invent information.
- **Fix:** Rewrote the task descriptions and `expected_output` to demand structured, evidence-based analysis grounded exclusively in the provided document.

- **Bug:** All tasks were incorrectly assigned to a single agent.
- **Fix:** Assigned each task to the most appropriate specialized agent (`financial_analyst`, `investment_advisor`, `risk_assessor`).

- **Bug:** The tasks were missing the `{file_path}` placeholder, preventing agents from locating the document.
- **Fix:** Added the `{file_path}` placeholder to all task descriptions.

### 4. Tooling (`tools.py`)

- **Bug:** The PDF reading tool was broken due to a missing `PyPDFLoader` import and an incorrect tool definition.
- **Fix:** Imported `PyPDFLoader` and correctly defined the `read_data_tool` with the `@tool` decorator.

- **Bug:** The file contained unimplemented and unnecessary tool classes.
- **Fix:** Removed the placeholder `InvestmentTool` and `RiskTool` classes, as their functionality is now handled by the specialized agents.
