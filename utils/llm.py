
"""LLM utilities for local Ollama and hosted Google Gemini."""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from config import OLLAMA_BASE_URL, OLLAMA_MODEL

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")


def _get_provider(provider=None):
    return (provider or "ollama").strip().lower()


def _get_google_api_key():
    key = os.getenv("GOOGLE_API_KEY")

    if key:
        return key

    # Streamlit Community Cloud Secrets fallback.
    try:
        import streamlit as st
        return st.secrets.get("GOOGLE_API_KEY", "")
    except Exception:
        return ""


def _make_ollama(
    temperature: float = 0.3,
    model: str = None,
    streaming: bool = False,
):
    from langchain_ollama import ChatOllama

    return ChatOllama(
        base_url=OLLAMA_BASE_URL,
        model=model or OLLAMA_MODEL,
        temperature=temperature,
    )


def _make_gemini(
    temperature: float = 0.3,
    model: str = None,
    streaming: bool = False,
):
    from langchain_google_genai import ChatGoogleGenerativeAI

    api_key = _get_google_api_key()
    if not api_key:
        raise RuntimeError(
            "GOOGLE_API_KEY is missing. Add it to your local .env "
            "or Streamlit Community Cloud Secrets."
        )

    return ChatGoogleGenerativeAI(
        model=model or GEMINI_MODEL,
        google_api_key=api_key,
        temperature=temperature,
    )


def get_llm(
    temperature: float = 0.3,
    streaming: bool = False,
    provider: str = None,
    model: str = None,
):
    selected = _get_provider(provider)

    if selected == "gemini":
        selected_model = model or GEMINI_MODEL
        print(f"[LLM] Provider: Gemini | Model: {selected_model}")
        return _make_gemini(temperature, selected_model, streaming)

    if selected == "ollama":
        selected_model = model or OLLAMA_MODEL
        print(f"[LLM] Provider: Ollama | Model: {selected_model}")
        return _make_ollama(temperature, selected_model, streaming)

    raise ValueError(f"Unsupported LLM provider: {selected}")


def get_llm_name(provider: str = None, model: str = None) -> str:
    selected = _get_provider(provider)

    if selected == "gemini":
        return f"Gemini ({model or GEMINI_MODEL})"

    return f"Ollama ({model or OLLAMA_MODEL})"


def list_available_providers() -> list[dict]:
    return [
        {
            "id": "ollama",
            "label": "Ollama (local)",
            "model": OLLAMA_MODEL,
            "active": True,
            "models": [
                "llama3.2",
                "llama3.1",
                "mistral",
                "codellama",
                "deepseek-coder",
            ],
        },
        {
            "id": "gemini",
            "label": "Google Gemini (cloud)",
            "model": GEMINI_MODEL,
            "active": True,
            "models": [GEMINI_MODEL],
        },
    ]


def _response_text(response) -> str:
    content = getattr(response, "content", response)

    if isinstance(content, str):
        return content.strip()

    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and item.get("text"):
                parts.append(item["text"])
        return "".join(parts).strip()

    return str(content).strip()


def invoke_llm(
    prompt: str,
    temperature: float = 0.3,
    provider: str = None,
    model: str = None,
) -> str:
    selected = _get_provider(provider)

    try:
        llm = get_llm(temperature, provider=selected, model=model)
        return _response_text(llm.invoke(prompt))
    except Exception as e:
        raise RuntimeError(
            f"{selected.capitalize()} request failed: {e}"
        ) from e


def invoke_llm_messages(
    messages: list,
    temperature: float = 0.3,
    provider: str = None,
    model: str = None,
) -> str:
    selected = _get_provider(provider)

    try:
        llm = get_llm(temperature, provider=selected, model=model)
        return _response_text(llm.invoke(messages))
    except Exception as e:
        raise RuntimeError(
            f"{selected.capitalize()} request failed: {e}"
        ) from e


def _stream_content(chunk):
    content = getattr(chunk, "content", chunk) or ""

    if isinstance(content, str):
        return content

    if isinstance(content, list):
        return "".join(
            item if isinstance(item, str)
            else item.get("text", "") if isinstance(item, dict)
            else ""
            for item in content
        )

    return str(content)


def stream_llm(
    prompt: str,
    temperature: float = 0.3,
    provider: str = None,
    model: str = None,
):
    selected = _get_provider(provider)

    try:
        llm = get_llm(
            temperature,
            streaming=True,
            provider=selected,
            model=model,
        )
        for chunk in llm.stream(prompt):
            content = _stream_content(chunk)
            if content:
                yield content
    except Exception as e:
        raise RuntimeError(
            f"{selected.capitalize()} stream failed: {e}"
        ) from e


def stream_llm_messages(
    messages: list,
    temperature: float = 0.3,
    provider: str = None,
    model: str = None,
):
    selected = _get_provider(provider)

    try:
        llm = get_llm(
            temperature,
            streaming=True,
            provider=selected,
            model=model,
        )
        for chunk in llm.stream(messages):
            content = _stream_content(chunk)
            if content:
                yield content
    except Exception as e:
        raise RuntimeError(
            f"{selected.capitalize()} stream failed: {e}"
        ) from e
