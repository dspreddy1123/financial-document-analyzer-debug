## Importing libraries and files
from crewai import Task

from agents import financial_analyst, investment_advisor, risk_assessor

## Creating a task to help solve user's query
analyze_financial_document = Task(
    # Instructions for Task demanding document-grounded, evidence-based financial analysis.
    description="""
Analyze the financial document at {file_path} to address the user's query: {query}.
Your *only* source of information is the provided document. Do not use any external knowledge.
Extract all financial figures, ratios, and insights directly from the document. If information is missing, explicitly state 'Information not found in document'.
""",

    expected_output="""
A financial analysis report formatted in Markdown, containing:

- **Key Financial Metrics:**  
  A table of key metrics (e.g., Revenue, Net Income, EPS, Deliveries, Cash) with their values and the exact page or section reference.  
  If a metric is not found, mark as 'Information not found in document'.

- **Financial Ratio Analysis:**  
  Calculate ratios (e.g., Debt-to-Equity, Current Ratio, Operating Margin) *only if all required numbers are in the document*.  
  Each ratio must show: calculation, result, and interpretation.  
  If inputs are missing, state 'Information not found in document'.

- **Direct Quotes on Performance:**  
  A section with verbatim quotes from the document about performance, risks, or outlook.  
  Include page/section references.

- **Conclusion:**  
  A summary of the company's financial state and trends based *strictly* on the document.  
  No speculation, no external context.
""",

    agent=financial_analyst,
    async_execution=False,
)

## Creating an investment analysis task
investment_analysis = Task(
    # Instructios for Task demanding an investment thesis grounded.
    description="""
Formulate an investment thesis for the company based solely on the document at {file_path}, in response to the user's query: {query}.
Do not use any external knowledge or speculation. Every claim must be tied to document evidence.
""",

    expected_output="""
An **Investment Thesis Memorandum** in Markdown format with:

- **Investment Thesis:**  
  A clear Buy/Hold/Sell/No Recommendation statement.  
  If a recommendation cannot be made due to missing data, explicitly state that.

- **Evidence-Based Rationale:**  
  A structured list of reasons, each supported by specific figures, metrics, or quotes from the document.  
  Cite page/section references.

- **Disclaimer:**  
  A standard disclaimer that the thesis is based solely on the provided document and not external analysis.
""",

    agent=investment_advisor,
    async_execution=False,
)

## Creating a risk assessment task
risk_assessment = Task(
    # Instructions for Task demanding extraction of explicitly stated risks.
    description="""
Extract all risk factors mentioned in the financial document at {file_path}, according to the user's query: {query}.
Your output must be strictly limited to risks explicitly described in the document. Do not infer or speculate.
""",

    expected_output="""
A **Risk Report** in Markdown format with:

- **Identified Risk Statements:**  
  A bullet-point list of direct risk statements quoted from the document.  
  Each must include its source location (page/section).

- **Summary:**  
  A concise overview of the main categories of risk, strictly based on the listed statements.  
  No external risk factors should be introduced.
""",

    agent=risk_assessor,
    async_execution=False,
)
