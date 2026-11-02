import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

repo_root = Path(r"c:\Ai_code\THLawDeka-mobile")

# 1. Update AGENTS.md
agents_path = repo_root / "AGENTS.md"
with open(agents_path, "r", encoding="utf-8") as f:
    agents_text = f.read()

target_be_guard = "Implement Long-Context Window Budgeting (emit SSE advisory on >64KB context recommending `/compact`)."
replacement_be_guard = "Implement Long-Context Window Budgeting (emit SSE advisory on >64KB context recommending `/compact`). Enforce Multi-Model Whitelist validation and `--model` CLI parameter pass-through (`GET /api/v1/models`)."

assert target_be_guard in agents_text, "target_be_guard not found in AGENTS.md"
agents_text = agents_text.replace(target_be_guard, replacement_be_guard, 1)

target_fe_guard = "Implement Partial Stream Recovery (`continueInterruptedStream`)"
replacement_fe_guard = "Implement Multi-Model Selection UI (Top App Bar Model Switcher & Modal BottomSheet), dynamic model discovery from `/api/v1/models` with offline fallback, model persistence in local SQLite (`selected_model` in sessions and `model_used` in messages). Implement Partial Stream Recovery (`continueInterruptedStream`)"

assert target_fe_guard in agents_text, "target_fe_guard not found in AGENTS.md"
agents_text = agents_text.replace(target_fe_guard, replacement_fe_guard, 1)

with open(agents_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(agents_text)
print("✓ Updated AGENTS.md")

# 2. Update .agents/skills/backend-development/SKILL.md
be_skill_path = repo_root / ".agents" / "skills" / "backend-development" / "SKILL.md"
with open(be_skill_path, "r", encoding="utf-8") as f:
    be_skill_text = f.read()

be_module10 = """
---

### Module 10: Multi-Model Discovery & Security Whitelist (`GET /api/v1/models`)

1. **Supported Model Whitelist**:
   - `gemini-3.8-flash-high` (Default, Fast, High Accuracy)
   - `gemini-3.8-flash-medium` (Fast, Balanced)
   - `gemini-3.8-flash-low` (Eco, Token-Saver)
   - `claude-sonnet-4-6` (Thinking, Deep Reasoning, Legal Analysis)
   - `claude-opus-4-6-thinking` (Thinking, Top Intelligence, High-Complexity Cases)
   - `gpt-oss-120b-medium` (Open Weights, Comparative Law)

2. **Security & Injection Guardrail**:
   - Validate model input with regex: `^[a-zA-Z0-9][a-zA-Z0-9._\-]{0,63}$`
   - Hard Reject any input not in `VALID_MODELS`
   - Pass safely to subprocess: `cmd.extend(["--model", req.model])` with `shell=False`
"""

be_skill_text = be_skill_text.strip() + "\n" + be_module10.strip() + "\n"
with open(be_skill_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(be_skill_text)
print("✓ Updated backend-development/SKILL.md with Module 10")

# 3. Update .agents/skills/frontend-development/SKILL.md
fe_skill_path = repo_root / ".agents" / "skills" / "frontend-development" / "SKILL.md"
with open(fe_skill_path, "r", encoding="utf-8") as f:
    fe_skill_text = f.read()

fe_module9 = """
---

### Module 9: Multi-Model Selection UI, Dynamic Discovery & SQLite Session Persistence

1. **Top App Bar Quick Model Switcher**:
   - Compact Chip component displaying active model: `[ ⚡ Gemini 3.8 Flash ▾ ]`
   - Tap action triggers `ModelSelectionBottomSheet` showing available models with category, badge, and description
2. **Dynamic Discovery & Offline Fallback**:
   - Fetch available models from `GET /api/v1/models` on network availability
   - Provide hardcoded offline fallback models if network is unreachable
3. **SQLite Model Persistence (`ChatDatabaseHelper.kt`)**:
   - Column `selected_model` in `chat_sessions` table
   - Column `model_used` in `chat_messages` table to render model attribution badge per message bubble
"""

fe_skill_text = fe_skill_text.strip() + "\n" + fe_module9.strip() + "\n"
with open(fe_skill_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(fe_skill_text)
print("✓ Updated frontend-development/SKILL.md with Module 9")
