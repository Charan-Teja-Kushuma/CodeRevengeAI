from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel            
from groq import Groq                      
import os                                  
import re                                  
from dotenv import load_dotenv             

# Milestone 2: Initializing the Model
load_dotenv()

# Activity 2.2: Configuration of the GROQ API
# Ensure GROQ_API_KEY is in your .env file
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Activity 2.3: Define model parameters
MODEL_CONFIG = {
    "model": "llama-3.3-70b-versatile",
    "temperature": 0.3,
    "max_tokens": 2000,
    "top_p": 0.9
}

app = FastAPI()

# Enable CORS for frontend development (Live Server)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the frontend directory to serve static files (CSS, JS, Images)
# Mount the frontend directory to serve static files (CSS, JS, Images)
app.mount("/static", StaticFiles(directory="../frontend"), name="static")


def parse_review_response(review_text: str) -> dict:
    """Parse the LLM response to extract structured data"""
    
    def count_issues(header_pattern, text):
        # Case insensitive search for the header
        section_match = re.search(fr'(?:###|\*\*)\s*{header_pattern}.*?(?=(?:###|\*\*)\s*(?:Critical|High|Medium|Low)|\Z)', text, re.IGNORECASE | re.DOTALL)
        if section_match:
            content = section_match.group(0)
            # Count bullets (- or *) or numbered lists (1.)
            return len(re.findall(r'(?:^|\n)\s*(?:-|\*|\d+\.)\s', content))
        return 0

    return {
        "critical_count": count_issues("Critical Issues", review_text),
        "high_count": count_issues("High Priority", review_text),
        "medium_count": count_issues("Medium Priority", review_text),
        "low_count": count_issues("Low Priority", review_text)
    }

# Activity 2: Create a function to review code

class CodeReviewRequest(BaseModel):
    code: str
    language: str
    focus_areas: list[str]

class CodeReviewResponse(BaseModel):
    review: str
    critical_count: int
    high_count: int
    medium_count: int
    low_count: int

@app.post("/api/review", response_model=CodeReviewResponse)
async def review_code(request: CodeReviewRequest):
    """Review code and provide suggestions using Groq API"""
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")

    focus_str = ", ".join(request.focus_areas)
    
    # Updated Elite Agent Prompt logic in main.py
    prompt = f"""
SYSTEM ROLE:
You are the **CodeRefine Sentinel AI**, an enterprise-grade autonomous code audit architect.
You combine the expertise of a Principal Software Architect, Security Engineer, and Performance Specialist with over 20 years of real-world system design experience. You are not a general assistant — you are a production-level code governance engine responsible for upgrading developer code into secure, optimized, and scalable software.

Your mindset:
• Assume code may be vulnerable until proven secure
• Prioritize security over performance, and performance over style
• Think in terms of scalability, maintainability, and real-world deployment
• Detect anti-patterns, unsafe practices, and inefficient logic
• Replace weak implementations with industry-standard solutions

You operate as the intelligence core of an AI-powered Code Review & Rewrite platform built with FastAPI and powered by ultra-fast LLM inference for real-time analysis.

MISSION:
Perform a deep technical audit of the provided code. Your job is not only to detect issues, but to refactor and elevate the code to production standards.

INPUT CODE ({request.language}):
{request.code}

FOCUS AREAS:
{focus_str}

STRICT RESPONSE FORMAT:

## EXECUTIVE SUMMARY
Provide a professional audit-style overview describing:
• Overall code health
• Security posture
• Performance level
• Maintainability status

## REFINED CODE
Provide the FULL rewritten version of the code using:
• Secure coding practices
• Parameterized queries where applicable
• Proper input validation and error handling
• Optimal time complexity
• Clean architecture and modular design
• Readable naming and documentation

The output must be production-ready and not partial.

## ISSUES FOUND
(You must list specific issues as bullet points using "- " inside the appropriate section. Do not use empty sections if no issues are found, but since you are critical, you likely will find issues.)

### Critical Issues
- [Issue Description]
- [Issue Description]

### High Priority
- [Issue Description]
- [Issue Description]

### Medium Priority
- [Issue Description]
- [Issue Description]

### Low Priority
- [Issue Description]
- [Issue Description]
"""


    # Sending request to Groq
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        **MODEL_CONFIG
    )
    
    review_text = response.choices[0].message.content
    print("\n\n=== RAW LLM RESPONSE START ===")
    print(review_text)
    print("=== RAW LLM RESPONSE END ===\n\n")
    counts = parse_review_response(review_text)
    print(f"Parsed Counts: {counts}")
    
    return {
        "review": review_text,
        **counts
    }

# Serving the login and main tool pages

@app.get("/styles.css")
async def serve_css():
    """Serve global styles at root for relative linking"""
    return FileResponse("../frontend/styles.css")

@app.get("/", response_class=HTMLResponse)
async def serve_landing():
    """Serve the landing page at root"""
    try:
        with open("../frontend/landing.html", "r", encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>landing.html not found</h1>")

@app.get("/login", response_class=HTMLResponse)
async def serve_login():
    """Serve the login page"""
    with open("../frontend/login.html", "r", encoding='utf-8') as f:
        return HTMLResponse(content=f.read())

@app.get("/app", response_class=HTMLResponse)
async def serve_tool():
    """Serve the main tool page after login"""
    try:
        with open("../frontend/index.html", "r", encoding='utf-8') as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(content="<h1>index.html not found</h1>")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"\n\n🚀 SERVER RUNNING AT: http://127.0.0.1:{port}/")
    print(f"👉 OPEN THIS URL IN YOUR BROWSER: http://127.0.0.1:{port}/\n\n")
    uvicorn.run(app, host="127.0.0.1", port=port)