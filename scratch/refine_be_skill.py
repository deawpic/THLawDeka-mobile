import sys
from pathlib import Path

be_path = Path(".agents/skills/backend-development/SKILL.md")
content = be_path.read_text(encoding="utf-8")

# Fix Module 1 SSE format: remove event: file
content = content.replace(
    '  - `event: file\\ndata: {"filename": "...", "download_url": "...", "size_bytes": 10485}\\n\\n`\n',
    ''
)

# Fix Module 3 Write on output: make 100% read-only
content = content.replace(
    'with Write permitted exclusively on `THLawDeka/output/`.',
    'with the entire workspace being 100% Immutable Read-Only (Server-Side Zero-Disk-Write Policy).'
)

# Add Tailscale Funnel Admin Shielding to Module 5
old_mod5 = """### Module 5: Admin Web UI (`backend/templates/admin.html`)
- Served at `GET /admin` via Jinja2 template.
- Protected by master `ADMIN_SECRET` environment variable.
- Features: View all issued keys, single-click copy key, Instant Revoke button, and Generate New Key modal."""

new_mod5 = """### Module 5: Admin Web UI (`backend/templates/admin.html`) & Tailscale Funnel Shielding
- Served at `GET /admin` via Jinja2 template.
- Protected by master `ADMIN_SECRET` environment variable.
- **Tailscale Funnel Admin Shielding**: When Tailscale Funnel is enabled to allow public Android clients to stream, restrict `/admin` and `/api/v1/admin/*` to Localhost (`127.0.0.1`) and Tailnet IPs (`100.64.0.0/10`) unless `ALLOW_PUBLIC_ADMIN=true`.
- Features: View all issued keys, single-click copy key, Instant Revoke button, and Generate New Key modal."""

assert old_mod5 in content, "old_mod5 not found"
content = content.replace(old_mod5, new_mod5)

# Update Module 7 with Funnel persistence
old_mod7 = "- **Tailscale Serve Persistence**: Ensure Tailscale serves with `--bg` so proxying survives reboot without manual intervention."
new_mod7 = "- **Tailscale Serve & Funnel Persistence**: Ensure Tailscale serves with `--bg` (`tailscale serve --bg https / http://127.0.0.1:8000`) and Funnel with `--bg` (`tailscale funnel --bg 443 on`) so proxying survives reboot without manual intervention."

assert old_mod7 in content, "old_mod7 not found"
content = content.replace(old_mod7, new_mod7)

be_path.write_text(content, encoding="utf-8")
print("Successfully refined backend-development/SKILL.md with Tailscale Funnel!")
