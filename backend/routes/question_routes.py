
from fastapi import APIRouter, HTTPException, Query

from backend.services.question_service import (
    get_all_questions,
    get_question_by_id,
    search_question_by_name,
)

router = APIRouter(prefix="/api/questions", tags=["Questions"])


@router.get("/")
def list_questions():
    return get_all_questions()


@router.get("/search")
def search_questions(name: str = Query(..., min_length=1)):
    question = search_question_by_name(name)

    if question is None:
        raise HTTPException(
            status_code=404,
            detail="LeetCode problem not found"
        )

    return question


@router.get("/{question_id}")
def get_question(question_id: str):
    question = get_question_by_id(question_id)

    if question is None:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    return question
