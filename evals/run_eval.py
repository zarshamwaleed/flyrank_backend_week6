import json
import requests
from datetime import datetime

def run_eval():
    with open("evals/cases.json", "r") as f:
        cases = json.load(f)
    
    total = len(cases)
    correct = 0
    
    for case in cases:
        try:
            response = requests.post(
                "http://localhost:8000/classify/",
                json={"text": case["input"]},
                timeout=30
            )
            if response.status_code == 200:
                result = response.json()
                if result.get("category") == case["category"]:
                    correct += 1
        except:
            pass
    
    print(f"Eval score: {correct}/{total}")
    print(f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    print(f"Prompt version: classify-v1")

if __name__ == "__main__":
    run_eval()