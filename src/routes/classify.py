import os
import json
import logging
from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from src.llm.schema import ClassifyInput, ClassifyOutput
from src.llm.client import call_model

router = APIRouter(prefix="/classify", tags=["LLM"])
logger = logging.getLogger(__name__)

STUB_RESPONSE = {
    "category": "other",
    "urgency": "normal",
    "confidence": 0.5,
    "reason": "Stub mode: simulated classification."
}

def parse_llm_response(raw_text: str):
    text = raw_text.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
    return json.loads(text.strip())

def quarantine_failed(input_data, raw_output, error, prompt_version):
    os.makedirs("logs", exist_ok=True)
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "input": input_data.text,
        "raw_output": raw_output,
        "error": str(error),
        "prompt_version": prompt_version
    }
    with open("logs/quarantine.jsonl", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

@router.post("/", response_model=ClassifyOutput)
async def classify_message(input_data: ClassifyInput):
    if os.environ.get("LLM_STUB") == "1":
        return STUB_RESPONSE
    
    if os.environ.get("LLM_ENABLED") == "0":
        return STUB_RESPONSE
    
    prompt_version = "classify-v1"
    raw_output = None
    
    try:
        raw_output = call_model(input_data.text)
        parsed = parse_llm_response(raw_output)
        validated = ClassifyOutput(**parsed)
        return validated.dict()
        
    except (json.JSONDecodeError, ValueError) as e:
        try:
            repair_prompt = f"""
The previous output was rejected. Error: {str(e)}
Broken output: {raw_output}
Return ONLY corrected JSON matching the schema.
"""
            repaired = call_model(input_data.text + "\n\n" + repair_prompt)
            parsed = parse_llm_response(repaired)
            validated = ClassifyOutput(**parsed)
            return validated.dict()
            
        except Exception as repair_error:
            quarantine_failed(input_data, raw_output, repair_error, prompt_version)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={"error": "Invalid output after repair", "quarantined": True}
            )
    
    except Exception as e:
        quarantine_failed(input_data, raw_output, e, prompt_version)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "Unexpected error"}
        )