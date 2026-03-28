from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import csv
import io
import os
from typing import List, Dict
from .agents.code_parsing_agent import CodeParsingAgent
from .agents.bug_detection_agent import BugDetectionAgent
from .agents.explanation_agent import ExplanationAgent
# from .agents.mcp_client import MCPClient  # We might need to mock or optimize this for Vercel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/process")
async def process_pipeline(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed")
    
    content = await file.read()
    decoded = content.decode('utf-8')
    csv_reader = csv.DictReader(io.StringIO(decoded))
    
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="OPENROUTER_API_KEY not set")

    # Initialize Agents
    parser = CodeParsingAgent(csv_path="") # Path not needed for live stream
    # For now, we mock MCP client results or use a simplified version
    # because the full MCP server won't run in a 10s serverless function
    class MockMCPClient:
        def search_documents(self, query): return []
        def connect(self): pass
        def disconnect(self): pass

    mcp_client = MockMCPClient()
    
    bug_detector = BugDetectionAgent(
        mcp_client=mcp_client,
        api_key=api_key,
        model="google/gemini-2.0-flash-001"
    )
    explainer = ExplanationAgent(
        api_key=api_key,
        model="google/gemini-2.0-flash-001"
    )

    results = []
    records = []
    for row in csv_reader:
        record = parser.parse_single(row)
        if record:
            records.append(record)
    
    # Run pipeline (limited for demo speed)
    for record in records[:5]: # Process first 5 samples for now
        detection = bug_detector.detect(record)
        explanation = explainer.explain(detection)
        results.append({
            "id": record["id"],
            "code": record["code"],
            "bug_line": explanation["bug_line"],
            "explanation": explanation["explanation"]
        })
    
    return {"results": results}
