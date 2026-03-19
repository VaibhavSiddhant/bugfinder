from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from analyzer.static import analyze
from model.predict import ml_predict

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeInput(BaseModel):
    code: str

@app.post("/analyze")
def analyze_code(input: CodeInput):
    static_issues = analyze(input.code)
    ml_result = ml_predict(input.code)

    return {
        "static": static_issues,
        "ml": ml_result,
        "has_issues": len(static_issues) > 0 or ml_result["bug"]
    }
