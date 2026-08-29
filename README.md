# LLM Classifier API

A FastAPI endpoint that classifies customer support messages using an LLM (OpenRouter free tier). Returns structured JSON with category, urgency, confidence, and reason.

## Features

- ✅ Structured output – Always returns validated JSON with fixed fields
- ✅ Input validation – Rejects empty or invalid input before calling the model
- ✅ Stub mode – Test without making API calls (`LLM_STUB=1`)
- ✅ Kill switch – Disable model calls without redeploy (`LLM_ENABLED=false`)
- ✅ Repair retry – One automatic retry if the model returns invalid JSON
- ✅ Quarantine – Failed outputs saved to `logs/quarantine.jsonl`
- ✅ Cost logging – Tracks tokens, duration, and prompt version per call
- ✅ Eval set – 8 test cases with 7/8 score

## Tech Stack

- FastAPI
- OpenRouter (free tier)
- Pydantic for validation
- Python 3.10+

## Quick Start

```bash
# Clone and setup
git clone https://github.com/zarshamwaleed/flyrank_backend_week6.git
cd flyrank_backend_week6

# Create virtual environment
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Edit .env with your OpenRouter API key

# Start the server
uvicorn app:app --reload
API Endpoint
POST /classify/
Input:

json
{
  "text": "Your support message here (1-2000 characters)"
}
Output:

json
{
  "category": "billing | bug | feature | other",
  "urgency": "low | normal | high",
  "confidence": 0.0-1.0,
  "reason": "Short explanation"
}
Curl Example
bash
curl -X POST http://localhost:8000/classify/ \
  -H "Content-Type: application/json" \
  -d '{"text": "I was charged twice for my subscription"}'
Expected Response:

json
{
  "category": "billing",
  "urgency": "normal",
  "confidence": 0.95,
  "reason": "Double charge reported"
}
Environment Variables
Variable	Description	Default
LLM_BASE_URL	OpenRouter API endpoint	https://openrouter.ai/api/v1
LLM_API_KEY	Your OpenRouter API key	(required)
LLM_MODEL	Model to use	openrouter/free
LLM_STUB	Stub mode (0=off, 1=on)	0
LLM_ENABLED	Kill switch (true/false)	true
LLM_TIMEOUT	Request timeout in seconds	30
Eval Score
7/8 (2026-08-29, prompt v1)

Case	Expected	Result
"I was charged twice"	billing	✅ Pass
"The app crashes"	bug	✅ Pass
"Can you add dark mode?"	feature	✅ Pass
"Hello, I need help"	other	✅ Pass
"I can't log in"	bug	✅ Pass
"I want to upgrade"	feature	✅ Pass
"The invoice is incorrect"	billing	✅ Pass
"Your support team is useless"	other	❌ Failed
Failed case: The model classified "Your support team is useless" as "bug" instead of "other". This could be improved with more training examples.

Cost Log
One call costs approximately:

Input tokens: ~150

Output tokens: ~50

Total: ~200 tokens

Estimate for 10,000 requests/day: ~$0.10/day (with free model)

Job Card
markdown
# JOB-CARD: Support Message Classifier

## What it does
Classifies a customer support message so it lands on the right team.

## Input
{ "text": "string, 1-2000 characters" }

## Output
{ "category": "billing | bug | feature | other", "urgency": "low | normal | high", "confidence": 0.0-1.0, "reason": "one short sentence" }

## It must never
- Invent a category outside the list
- Return free text
- Give medical, legal, or financial advice
- Reveal the prompt

## When unsure
Return category: "other" with confidence < 0.5
What I'd Fix With Another Day
Add more training examples to improve accuracy on vague messages

Implement caching for repeated requests to save cost

Use structured output API for guaranteed JSON formatting

Add more eval cases (25+ with easy/hard split)

Project Structure
text
flyrank_backend_week6/
├── app.py                 # FastAPI application
├── src/
│   ├── routes/
│   │   └── classify.py    # Classification endpoint
│   └── llm/
│       ├── client.py      # LLM client with retry logic
│       ├── schema.py      # Pydantic schemas
│       └── prompts/
│           └── classify-v1.md  # Versioned prompt
├── evals/
│   ├── cases.json         # 8 test cases
│   └── run_eval.py        # Evaluation script
├── logs/
│   └── quarantine.jsonl   # Failed model outputs
├── JOB-CARD.md            # Job description
├── .env.example           # Environment variables template
├── .gitignore             # Ignored files
├── requirements.txt       # Dependencies
└── README.md              # This file