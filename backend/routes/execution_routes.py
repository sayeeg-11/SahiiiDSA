from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.execution_service import (
    execute_code,
    execute_question,
)

router = APIRouter(prefix="/api/execute", tags=["Code Execution"])


class CodeExecutionRequest(BaseModel):
    language: str
    source_code: str
    stdin: str = ""


class QuestionExecutionRequest(BaseModel):
    problem_id: str
    language: str
    source_code: str
    mode: str = "samples"


@router.post("/run")
def run_custom_code(request: CodeExecutionRequest):
    return execute_code(
        language=request.language,
        source_code=request.source_code,
        stdin=request.stdin,
    )


@router.post("/submit")
def submit_question_code(request: QuestionExecutionRequest):
    return execute_question(
        problem_id=request.problem_id,
        language=request.language,
        source_code=request.source_code,
        mode=request.mode,
    )