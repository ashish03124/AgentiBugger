"""
Agent 1 — Code Parsing Agent (Web Version)
"""
import csv

class CodeParsingAgent:
    def __init__(self, csv_path: str):
        self.csv_path = csv_path

    def parse_single(self, row: dict) -> dict:
        try:
            sample_id = row.get("ID", "").strip()
            explanation_hint = row.get("Explanation", "").strip()
            context = row.get("Context", "").strip()
            code = row.get("Code", "").strip()
            correct_code = row.get("Correct Code", "").strip()

            if not sample_id or not code:
                return None

            code_lines = code.split("\n")
            numbered_code = "\n".join(
                f"{i+1}: {line}" for i, line in enumerate(code_lines)
            )

            return {
                "id": sample_id,
                "explanation_hint": explanation_hint,
                "context": context,
                "code": code,
                "correct_code": correct_code,
                "numbered_code": numbered_code,
                "total_lines": len(code_lines),
            }
        except Exception:
            return None
