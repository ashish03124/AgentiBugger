"""
Agent 3 -- Explanation Agent (Web Version)
"""
import requests
import json

class ExplanationAgent:
    def __init__(self, api_key: str, model: str = "google/gemini-2.0-flash-001"):
        self.api_key = api_key
        self.model = model
        self.api_url = "https://openrouter.ai/api/v1/chat/completions"

    def explain(self, detection_result: dict) -> dict:
        prompt = f"""Explain why line {detection_result['bug_line']} has a bug.
Code:
{detection_result['numbered_code']}
Explanation Hint: {detection_result.get('explanation_hint')}
Docs Context: {detection_result.get('doc_context')}
Keep it concise (2 sentences)."""

        try:
            response = requests.post(
                url=self.api_url,
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                data=json.dumps({
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.3,
                }),
                timeout=30
            )
            explanation = response.json()["choices"][0]["message"]["content"].strip()
            return {
                "id": detection_result["id"],
                "bug_line": detection_result["bug_line"],
                "explanation": explanation
            }
        except Exception:
            return {"id": detection_result["id"], "bug_line": detection_result["bug_line"], "explanation": "Error generating explanation."}
