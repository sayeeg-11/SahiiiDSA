
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path


SUPPORTED_LANGUAGES = {"python", "c", "cpp"}
DEFAULT_TIMEOUT = 3
MAX_TIMEOUT = 10
MAX_DISPLAY_CHARS = 12000


def _result(
    status: str,
    stdout: str = "",
    stderr: str = "",
    return_code: int | None = None,
    duration_ms: int = 0,
) -> dict:
    return {
        "status": status,
        "stdout": stdout[:MAX_DISPLAY_CHARS],
        "stderr": stderr[:MAX_DISPLAY_CHARS],
        "return_code": return_code,
        "duration_ms": duration_ms,
    }


def run_code(
    language: str,
    source_code: str,
    stdin: str = "",
    timeout_seconds: int = DEFAULT_TIMEOUT,
) -> dict:
    """Compile and run trusted student code locally.

    This is a development runner, NOT a security sandbox.
    Only run code you trust.
    """
    language = language.strip().lower()

    if language not in SUPPORTED_LANGUAGES:
        return _result("error", stderr=f"Unsupported language: {language}")

    if not source_code.strip():
        return _result("error", stderr="Please enter some code.")

    timeout_seconds = max(1, min(int(timeout_seconds), MAX_TIMEOUT))

    with tempfile.TemporaryDirectory(prefix="sahiiidsa_") as temp:
        work_dir = Path(temp)

        if language == "python":
            source_file = work_dir / "main.py"
            source_file.write_text(source_code, encoding="utf-8")
            run_command = [sys.executable, "-I", str(source_file)]

        else:
            is_cpp = language == "cpp"
            source_file = work_dir / ("main.cpp" if is_cpp else "main.c")
            executable = work_dir / ("main.exe" if os.name == "nt" else "main")

            source_file.write_text(source_code, encoding="utf-8")

            compiler = "g++" if is_cpp else "gcc"
            compile_command = [
                compiler,
                str(source_file),
                "-o",
                str(executable),
            ]

            if is_cpp:
                compile_command.insert(1, "-std=c++17")
            else:
                compile_command.insert(1, "-std=c11")

            started = time.perf_counter()

            try:
                compiled = subprocess.run(
                    compile_command,
                    cwd=work_dir,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                    errors="replace",
                    timeout=timeout_seconds,
                    shell=False,
                )
            except FileNotFoundError:
                return _result(
                    "error",
                    stderr=f"{compiler} was not found. Check your compiler PATH.",
                )
            except subprocess.TimeoutExpired:
                return _result(
                    "compile_timeout",
                    stderr="Compilation exceeded the time limit.",
                    duration_ms=int((time.perf_counter() - started) * 1000),
                )

            compile_ms = int((time.perf_counter() - started) * 1000)

            if compiled.returncode != 0:
                return _result(
                    "compile_error",
                    stderr=compiled.stderr or compiled.stdout,
                    return_code=compiled.returncode,
                    duration_ms=compile_ms,
                )

            run_command = [str(executable)]

        started = time.perf_counter()

        try:
            completed = subprocess.run(
                run_command,
                input=stdin,
                cwd=work_dir,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=timeout_seconds,
                shell=False,
            )

            duration_ms = int((time.perf_counter() - started) * 1000)

            if completed.returncode != 0:
                return _result(
                    "runtime_error",
                    stdout=completed.stdout,
                    stderr=completed.stderr or "Program exited with an error.",
                    return_code=completed.returncode,
                    duration_ms=duration_ms,
                )

            return _result(
                "success",
                stdout=completed.stdout,
                stderr=completed.stderr,
                return_code=completed.returncode,
                duration_ms=duration_ms,
            )

        except subprocess.TimeoutExpired as exc:
            duration_ms = int((time.perf_counter() - started) * 1000)
            stdout = exc.stdout or ""
            stderr = exc.stderr or ""

            if isinstance(stdout, bytes):
                stdout = stdout.decode("utf-8", errors="replace")
            if isinstance(stderr, bytes):
                stderr = stderr.decode("utf-8", errors="replace")

            return _result(
                "timeout",
                stdout=stdout,
                stderr=f"Execution exceeded {timeout_seconds} seconds.",
                duration_ms=duration_ms,
            )
        except OSError as exc:
            return _result("error", stderr=str(exc))
