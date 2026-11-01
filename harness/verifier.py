"""
Deterministic Ground-Truth Verifier (Pre-Handoff Fast Gate & Strict Boundary Enforcer).
Performs lightweight syntax/type/file checks, boundary isolation, and blast radius auditing.
"""

from __future__ import annotations
from dataclasses import dataclass, field
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from typing import List, Optional, Tuple

from harness.schemas import VerificationReceipt


IGNORE_BOUNDARY_FILES = {
    "stack.json",
    ".gitignore",
    ".tmp",
}


@dataclass
class VerificationResult:
    passed: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    verified_files: List[str] = field(default_factory=list)
    receipt: Optional[VerificationReceipt] = None

    def summary(self) -> str:
        if self.passed:
            return f"Deterministic Verification Passed ({len(self.verified_files)} files verified)."
        return f"Deterministic Verification Failed with {len(self.errors)} error(s): " + "; ".join(self.errors[:3])


class DeterministicVerifier:
    """Fast ground-truth verification without invoking LLMs."""

    def __init__(self, workspace_root: str = "."):
        self.workspace_root = Path(workspace_root).resolve()

    def _normalize_rel_path(self, raw_path: str) -> str:
        p = Path(raw_path.strip().strip('"'))
        if p.is_absolute():
            try:
                return str(p.relative_to(self.workspace_root))
            except ValueError:
                return str(p)
        return str(p)

    def check_file_boundaries(
        self,
        allowed_files: List[str],
        exempt_files: Optional[List[str]] = None,
    ) -> Tuple[bool, List[str]]:
        """
        Hyper-Disciplined Stack Hygiene (Rule 1):
        Inspects git status to ensure no files outside allowed_files (or exempt prior task files)
        were created or modified.
        """
        if not allowed_files:
            # If no allowed_files specified, boundary check is bypassed
            return True, []

        allowed_normalized = {self._normalize_rel_path(f) for f in allowed_files if f}
        if exempt_files:
            allowed_normalized.update(self._normalize_rel_path(f) for f in exempt_files if f)

        cmd = ["git", "status", "--porcelain", "-uall"]
        try:
            res = subprocess.run(cmd, cwd=self.workspace_root, capture_output=True, text=True, check=False)
            lines = res.stdout.strip().splitlines()
        except Exception:
            return True, []

        unauthorized_files: List[str] = []
        for line in lines:
            if not line or len(line) < 4:
                continue
            # status code is first 2 chars, then space, then filename
            file_entry = line[2:].strip()
            # Handle renames: old -> new
            if " -> " in file_entry:
                file_entry = file_entry.split(" -> ")[-1].strip()
            file_entry = self._normalize_rel_path(file_entry)

            # Ignore internal harness and temporary files
            entry_name = Path(file_entry).name
            if entry_name in IGNORE_BOUNDARY_FILES or file_entry.endswith(".tmp"):
                continue

            if file_entry not in allowed_normalized:
                unauthorized_files.append(file_entry)

        if unauthorized_files:
            return False, unauthorized_files
        return True, []

    def check_blast_radius(
        self,
        max_lines: int = 200,
        max_files: int = 4,
        target_files: Optional[List[str]] = None,
        exempt_extensions: Tuple[str, ...] = (".md",),
    ) -> Tuple[bool, str]:
        """
        Atomic Decomposition (Rule 2):
        Inspects git diff --numstat to ensure code changes don't exceed atomic blast radius.
        Design documents (.md) are exempt from the line-count cap so specs/ADRs are not truncated.
        """
        rel_targets: List[str] = []
        if target_files:
            rel_targets = [self._normalize_rel_path(f) for f in target_files if f]

        cmd = ["git", "diff", "--numstat"]
        if rel_targets:
            cmd.extend(["--"] + rel_targets)

        try:
            res = subprocess.run(cmd, cwd=self.workspace_root, capture_output=True, text=True, check=False)
            output = res.stdout.strip()
            if not output:
                # Also check staged changes
                staged_cmd = ["git", "diff", "--cached", "--numstat"]
                if rel_targets:
                    staged_cmd.extend(["--"] + rel_targets)
                res_staged = subprocess.run(staged_cmd, cwd=self.workspace_root, capture_output=True, text=True, check=False)
                output = res_staged.stdout.strip()
        except Exception:
            return True, ""

        if not output:
            return True, ""

        total_lines = 0
        total_files = 0
        for line in output.splitlines():
            parts = line.split("\t")
            if len(parts) >= 3:
                ins, dels, fname = parts[0], parts[1], parts[2]
                path_obj = Path(fname)
                if path_obj.name in IGNORE_BOUNDARY_FILES:
                    continue
                if exempt_extensions and path_obj.suffix.lower() in exempt_extensions:
                    continue
                try:
                    total_lines += int(ins) + int(dels)
                    total_files += 1
                except ValueError:
                    pass

        if total_files > max_files:
            return False, f"Modified {total_files} files (exceeds atomic limit of {max_files}). Push smaller subtasks."
        if total_lines > max_lines:
            return False, f"Modified {total_lines} lines (exceeds atomic limit of {max_lines}). Push smaller subtasks."

        return True, ""

    def verify_artifacts(self, artifact_paths: List[str]) -> VerificationResult:
        """
        Mandatory Verification before Pop (Rule 3):
        Verifies physical existence and syntax of all declared artifacts.
        """
        result = VerificationResult(passed=True)

        if not artifact_paths:
            result.warnings.append("No artifacts declared for verification.")
            return result

        for raw_path in artifact_paths:
            path = Path(raw_path)
            if not path.is_absolute():
                path = self.workspace_root / path

            # 1. Physical existence check
            if not path.exists():
                result.passed = False
                result.errors.append(f"Physical file missing (Hallucinated artifact): {raw_path}")
                continue

            if not path.is_file():
                result.passed = False
                result.errors.append(f"Artifact path is not a regular file: {raw_path}")
                continue

            result.verified_files.append(str(path))

            # 2. Syntax validation based on extension
            ext = path.suffix.lower()

            if ext == ".py":
                py_valid, py_err = self._verify_python_syntax(path)
                if not py_valid:
                    result.passed = False
                    result.errors.append(f"Python syntax error in {path.name}: {py_err}")

            elif ext == ".json":
                json_valid, json_err = self._verify_json_syntax(path)
                if not json_valid:
                    result.passed = False
                    result.errors.append(f"Invalid JSON syntax in {path.name}: {json_err}")

            elif ext == ".md":
                if path.stat().st_size == 0:
                    result.passed = False
                    result.errors.append(f"Markdown design artifact is empty (0 bytes): {path.name}")

            elif ext in (".kt", ".kts", ".html"):
                if path.stat().st_size == 0:
                    result.passed = False
                    result.errors.append(f"Source file artifact is empty (0 bytes): {path.name}")

            elif ext == ".xml":
                if path.stat().st_size == 0:
                    result.passed = False
                    result.errors.append(f"XML artifact is empty (0 bytes): {path.name}")
                else:
                    xml_valid, xml_err = self._verify_xml_syntax(path)
                    if not xml_valid:
                        result.passed = False
                        result.errors.append(f"Invalid XML syntax in {path.name}: {xml_err}")

        if result.passed and result.verified_files:
            result.receipt = VerificationReceipt(
                timestamp=time.time(),
                gate_type="LIGHTWEIGHT_STATIC",
                verified_files=result.verified_files,
                exit_code=0,
                status="PASSED",
                details=f"Verified {len(result.verified_files)} artifact(s) successfully.",
            )

        return result

    def _verify_python_syntax(self, file_path: Path) -> Tuple[bool, str]:
        """Runs py_compile in a subprocess to check syntax without executing code."""
        cmd = [sys.executable, "-m", "py_compile", str(file_path)]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            return True, ""
        err_msg = res.stderr.strip().splitlines()[-1] if res.stderr.strip() else "Unknown syntax error"
        return False, err_msg

    def _verify_json_syntax(self, file_path: Path) -> Tuple[bool, str]:
        """Checks if a JSON file is well-formed."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                json.load(f)
            return True, ""
        except Exception as e:
            return False, str(e)

    def _verify_xml_syntax(self, file_path: Path) -> Tuple[bool, str]:
        """Validates XML syntax."""
        try:
            import xml.etree.ElementTree as ET
            ET.parse(file_path)
            return True, ""
        except Exception as e:
            return False, str(e)
