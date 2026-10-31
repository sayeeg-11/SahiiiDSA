
from ingestion.leetcode_client import LeetCodeClient

leetcode_client = LeetCodeClient()


def get_all_questions():
    """
    Return questions available in the offline cache.

    The current LeetCodeClient supports individual problem lookup,
    but does not yet provide a complete problemset listing.
    """

    from ingestion.leetcode_client import _load_offline_cache

    cache = _load_offline_cache()

    questions = []

    for slug, question in cache.items():
        questions.append({
            "id": slug,
            "title": question.get("title", slug),
            "number": question.get("number", "?"),
            "difficulty": question.get("difficulty", "Medium"),
            "tags": question.get("tags", []),
        })

    return questions


def get_question_by_id(question_id: str):
    """
    Fetch complete problem details using LeetCodeClient.
    """

    question = leetcode_client.get_problem_description(question_id)

    if not question:
        return None

    return {
        "id": question.get("slug", question_id),
        "title": question.get("title", "Unknown"),
        "number": question.get("number", "?"),
        "difficulty": question.get("difficulty", "Medium"),
        "tags": question.get("tags", []),
        "description": question.get("description", ""),
        "examples": question.get("examples", ""),
        "hints": question.get("hints", []),
        "source": question.get("source", "unknown"),
    }


def search_question_by_name(name: str):
    """
    Search for a problem by its title.
    """

    question = leetcode_client.search_problem_by_name(name)

    if not question:
        return None

    return {
        "id": question.get("slug", ""),
        "title": question.get("title", "Unknown"),
        "number": question.get("number", "?"),
        "difficulty": question.get("difficulty", "Medium"),
        "tags": question.get("tags", []),
        "description": question.get("description", ""),
        "examples": question.get("examples", ""),
        "hints": question.get("hints", []),
        "source": question.get("source", "unknown"),
    }
