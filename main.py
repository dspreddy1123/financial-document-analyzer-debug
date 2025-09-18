from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import uuid
from dotenv import load_dotenv

from crewai import Crew, Process
from agents import financial_analyst, investment_advisor, risk_assessor
from task import analyze_financial_document, investment_analysis, risk_assessment

# Load environment variables
load_dotenv()

# --- FastAPI App ---
app = FastAPI(title="Financial Document Analyzer")

app.mount("/static", StaticFiles(directory="public"), name="static")

def run_crew(query: str, file_path: str):
    """To run the whole crew"""
    print(f"Running crew with query: {query} and file_path: {file_path}")
    financial_crew = Crew(
        agents=[financial_analyst, investment_advisor, risk_assessor],
        tasks=[analyze_financial_document, investment_analysis, risk_assessment],
        process=Process.sequential,
    )
    
    result = financial_crew.kickoff({'query': query, 'file_path': file_path})
    print(f"Crew finished with result: {result}")

    return {
        "financial_analysis": financial_crew.tasks[0].output.raw,
        "investment_advice": financial_crew.tasks[1].output.raw,
        "risk_assessment": financial_crew.tasks[2].output.raw,
    }

@app.get("/", response_class=FileResponse)
async def read_index():
    """Serve the main HTML file"""
    return "public/index.html"

@app.post("/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """Analyze financial document and provide comprehensive investment recommendations"""
    
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        os.makedirs("data", exist_ok=True)
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        if query=="" or query is None:
            query = "Analyze this financial document for investment insights"
            
        response = run_crew(query=query.strip(), file_path=file_path)
        
        return {
            "status": "success",
            "query": query,
            "analysis": response,
            "file_processed": file.filename
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")
    
    finally:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
