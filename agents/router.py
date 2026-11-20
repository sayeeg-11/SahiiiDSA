"""
Router — LLM-based intent classification for user messages.

Design rationale:
  LLM classification is more robust than regex for DSA mentoring: it handles
  colloquial phrasing, mixed intents, and novel formulations that fixed patterns
  miss. The trade-off is one small extra LLM call per message (~0.3 s on Gemini
  flash), which is acceptable given the mentor already calls the LLM for the
  actual response.

  Two unambiguous signals are handled before the LLM call to avoid unnecessary
  latency:
    • Code block present (``` markers) → CODE_FIX immediately
    • Bare integer input               → QUESTION_LOOKUP immediately
"""
import re
import sys
from enum import Enum
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


class Intent(Enum):
    """Possible user intents."""
    QUESTION_LOOKUP  = "question_lookup"   # "What is Two Sum?" / "LeetCode 121"
    CODE_FIX         = "code_fix"          # "Fix my code" / code block present
    HINT_REQUEST     = "hint_request"      # "Give me a hint" / "I'm stuck"
    CONCEPT_QUESTION = "concept_question"  # "Explain sliding window" / "When to use DP?"
    GENERAL_CHAT     = "general_chat"      # Greetings, follow-ups, anything else
    SOLUTION_REQUEST = "solution_request"  # "Show me the solution" / "I give up"


# ── LLM Classification Prompt ────────────────────────────────────


_ROUTER_PROMPT = """\
You are an intent classifier for SahiiiDSA, an intelligent DSA learning mentor.

Your task is to identify what the student wants the system to DO.
Choose exactly ONE intent from the six categories below.

==================== INTENT DEFINITIONS ====================

1. QUESTION_LOOKUP
The student wants to find, open, identify, or retrieve a specific
DSA/LeetCode problem.

Examples:
- What is Two Sum?
- Tell me about Merge Intervals.
- Open LeetCode problem 121.
- Find the Best Time to Buy and Sell Stock problem.
- I want to solve problem 42.

Important:
A named coding problem is a problem lookup, even when the student
uses words like "what is", "tell me about", or "explain the problem".

2. CODE_FIX
The student wants help debugging, correcting, or understanding
an error in their own code.

Examples:
- Fix my code.
- Why is my C++ code failing?
- My program gives the wrong output.
- Find the bug in my implementation.
- Why am I getting a compilation error?

Important:
An explicit request to debug or fix code belongs here, even if
the student has not pasted the code yet.

3. HINT_REQUEST
The student wants guidance without receiving the complete solution.

Examples:
- Give me a hint.
- I'm stuck. Where should I start?
- Guide me towards an approach.
- Give me a small nudge.
- Don't reveal the answer.

Important:
The student wants help progressing independently, not the final code.

4. SOLUTION_REQUEST
The student explicitly wants the complete answer, implementation,
or final solution.

Examples:
- Show me the complete solution.
- Give me the full C++ code.
- I give up. Give me the answer.
- Reveal the final solution.
- I want the complete implementation.

Important:
An explicit request for the final answer takes priority over
a general request for help.

5. CONCEPT_QUESTION
The student wants to learn or understand a general DSA concept,
algorithm, technique, or theoretical principle.

Examples:
- Explain the sliding window technique.
- What is dynamic programming?
- When should I use BFS?
- Explain binary search time complexity.
- What is the difference between stack and queue?

Important:
The question is about a general concept, not about retrieving
a particular coding problem or debugging the student's code.

6. GENERAL_CHAT
The message is a greeting, acknowledgement, thank-you, casual
conversation, or follow-up that does not clearly request one
of the five actions above.

Examples:
- Hello Sahiii.
- Thank you for helping me.
- Okay, I understand now.
- Can you explain that again?
- That makes sense.
- Nice, let's continue.

Important:
If a message depends on previous conversation context that is
not provided, do not invent that context. Classify based on
the current message alone.

==================== CLASSIFICATION PRIORITIES ====================

When a message appears to match multiple categories, use these rules:

1. Explicit request for complete answer/code → SOLUTION_REQUEST.
2. Explicit debugging or code correction request → CODE_FIX.
3. Request for a hint without the final answer → HINT_REQUEST.
4. Request to retrieve or identify a named coding problem → QUESTION_LOOKUP.
5. General DSA theory or algorithm explanation → CONCEPT_QUESTION.
6. Greeting, acknowledgement, or unclear conversational follow-up
   → GENERAL_CHAT.

Do not classify a message merely by individual keywords.
Understand the student's primary objective.

==================== STUDENT MESSAGE ====================

{message}

==================== OUTPUT RULE ====================

Return exactly ONE category name from this list:

QUESTION_LOOKUP
CODE_FIX
HINT_REQUEST
CONCEPT_QUESTION
GENERAL_CHAT
SOLUTION_REQUEST

Do not provide explanations, punctuation, or additional text.
"""


_VALID_INTENTS = {i.name for i in Intent}



def detect_intent(message: str, has_code_block: bool = False) -> Intent:
    """
    Hybrid intent classification:
    1. Deterministic rules for unambiguous messages.
    2. LLM classification for nuanced messages.
    3. GENERAL_CHAT fallback if LLM classification fails.
    """

    msg = message.strip()
    lower_msg = msg.lower()

    # Fast-path 1: Explicit code block
    if has_code_block or "```" in message:
        return Intent.CODE_FIX

    # Fast-path 2: Bare problem number
    if re.fullmatch(r"\d+", msg):
        return Intent.QUESTION_LOOKUP

    # Fast-path 3: Explicit complete solution request
    solution_patterns = [
        r"\b(full|complete|entire)\s+(solution|answer|code|implementation)\b",
        r"\b(show|give|provide|reveal)\s+(me\s+)?(the\s+)?(solution|answer)\b",
        r"\bi give up\b",
    ]
    # Explicitly requesting guidance instead of the answer
    hint_override_patterns = [
        r"\bdon't give me the answer\b",
        r"\bdo not give me the answer\b",
        r"\bjust a nudge\b",
        r"\bwithout (giving|revealing) (me )?(the )?answer\b",
    ]

    if any(re.search(pattern, lower_msg) for pattern in hint_override_patterns):
        return Intent.HINT_REQUEST

    if any(re.search(pattern, lower_msg) for pattern in solution_patterns):
        return Intent.SOLUTION_REQUEST

    # Fast-path 4: Explicit debugging request
    code_fix_patterns = [
        r"\b(debug|debugging)\b",
        r"\bfix\s+(my|this|the)\s+code\b",
        r"\b(code|program|implementation)\s+(is\s+)?(failing|broken)\b",
        r"\bwrong output\b",
        r"\bcompilation error\b",
        r"\bsyntax error\b",
    ]

    if any(re.search(pattern, lower_msg) for pattern in code_fix_patterns):
        return Intent.CODE_FIX

    # Fast-path 5: Explicit hint or guidance request
    hint_patterns = [
        r"\bi'?m stuck\b",
        r"\bwhere should i start\b",
        r"\bwhere do i start\b",
        r"\bneed\s+(a\s+)?hint\b",
        r"\b(give|provide)\s+(me\s+)?(a\s+)?hint\b",
        r"\bjust a nudge\b",
        r"\bguide me\b",
        r"\bhelp me approach\b",
        r"\bwithout (giving|revealing) (me )?(the )?answer\b",
    ]

    if any(re.search(pattern, lower_msg) for pattern in hint_patterns):
        return Intent.HINT_REQUEST

    # Fast-path 6: Standalone greetings and acknowledgements
    greeting_patterns = [
        r"(hi|hello|hey)(\s+sahiii)?[!. ]*",
        r"good (morning|afternoon|evening)[!. ]*",
        r"(thanks|thank you)(\s+sahiii)?[!. ]*",
        r"okay[!. ]*",
        r"got it[!. ]*",
    ]

    if any(re.fullmatch(pattern, lower_msg) for pattern in greeting_patterns):
        return Intent.GENERAL_CHAT

    # LLM classification for nuanced messages
    try:
        from utils.llm import invoke_llm

        print(
            f"[Router] Classifying: \"{message[:80]}{'...' if len(message) > 80 else ''}\"",
            flush=True
        )

        prompt = _ROUTER_PROMPT.format(message=msg)
        response = invoke_llm(prompt, temperature=0.0).strip().upper()

        matches = re.findall(r"\b[A-Z_]+\b", response)

        response = next(
            (word for word in matches if word in _VALID_INTENTS),
            ""
        )

        if response:
            print(f"[Router] Intent → {response}", flush=True)
            return Intent[response]

        print(f"[Router] Unrecognised response '{response}', falling back to GENERAL_CHAT")

    except Exception as e:
        print(f"[Router] LLM classification failed ({e}), falling back to GENERAL_CHAT")

    return Intent.GENERAL_CHAT


# ── Helper: extract problem identifier ───────────────────────────

def extract_problem_identifier(message: str) -> Optional[str]:
    """
    Extract a LeetCode problem name or number from a user message.
    Returns the identifier string or None.
    """
    msg = message.strip()

    # "LeetCode 121" / "LC #1" / "Problem 42"
    match = re.search(r"(?:leetcode|lc|problem)\s*#?\s*(\d+)", msg, re.IGNORECASE)
    if match:
        return match.group(1)

    # Pure number
    if re.match(r"^\d+$", msg):
        return msg

    # "1. Two Sum" format
    match = re.match(r"^#?(\d+)[\.\s]", msg)
    if match:
        return msg

    # Problem name in quotes
    match = re.search(r"['\"](.+?)['\"]", msg)
    if match:
        return match.group(1)

    # "What is Two Sum" / "Tell me about Merge Intervals"
    for prefix in [
        "what is ", "describe ", "explain ", "tell me about ",
        "look up ", "find ", "fetch ",
    ]:
        if msg.lower().startswith(prefix):
            return msg[len(prefix):].strip().strip("?").strip()

    return msg if len(msg.split()) <= 6 else None


# ── Helper: extract code block ────────────────────────────────────

def extract_code_block(message: str) -> Optional[str]:
    """Extract code from a markdown code block in the message."""
    match = re.search(r"```(?:\w+)?\s*\n?(.*?)```", message, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None
