"""
Agent 2 -- Bug Detection Agent (Web Version)
"""
import requests
import json

class BugDetectionAgent:
    def __init__(self, mcp_client, api_key: str, model: str = "google/gemini-2.0-flash-001"):
        self.mcp_client = mcp_client
        self.api_key = api_key
        self.model = model
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"

    def detect(self, parsed_record: dict) -> dict:
        search_query = f"{parsed_record.get('context', '')} {parsed_record.get('explanation_hint', '')}"
        docs = self.mcp_client.search_documents(search_query[:500])
        
        doc_context = ""
        if not docs:
            doc_context = "No additional context found."
        else:
            doc_context = "\n\n".join([f"Docs: {d.get('text', '')}" for d in docs[:3]])

        prompt = f"""Identify the EXACT line number of the bug. 
Code:
{parsed_record['numbered_code']}
Context: {parsed_record.get('context')}
Hint: {parsed_record.get('explanation_hint')}
Docs: {doc_context}
Return ONLY the line number(s)."""

        try:
            response = requests.post(
                url=self.api_url,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                data=json.dumps({
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.0,
                }),
                timeout=30
            )
            return {
                "id": parsed_record["id"],
                "bug_line": response.json()["choices"][0]["message"]["content"].strip(),
                "numbered_code": parsed_record["numbered_code"],
                "context": parsed_record["context"],
                "explanation_hint": parsed_record["explanation_hint"],
                "doc_context": doc_context
            }
        except Exception:
            return {"id": parsed_record["id"], "bug_line": "Unknown", "numbered_code": parsed_record["numbered_code"]}
