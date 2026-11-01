import sqlite3
import secrets
import hashlib
import json
from pathlib import Path
from datetime import datetime, timedelta, timezone

DB_PATH = Path(__file__).resolve().parent / "keys.db"

class AuthDB:
    def __init__(self, db_path: Path = DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        # เปิดโหมด Write-Ahead Logging (WAL) เพื่อ Non-blocking Concurrency
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS api_keys (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key_token TEXT UNIQUE NOT NULL,
                    user_name TEXT NOT NULL,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    revoked_at TIMESTAMP NULL
                );
            """)
            # ตารางแคชผลวิเคราะห์คำถามกฎหมายที่พบบ่อย (Legal Response Cache)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS legal_cache (
                    query_hash TEXT PRIMARY KEY,
                    query_text TEXT NOT NULL,
                    cached_events TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL
                );
            """)
            conn.commit()

    def generate_key(self, user_name: str) -> str:
        """สร้างกุญแจความปลอดภัยสูง เช่น thlaw_live_7a8f9c2d..."""
        token = f"thlaw_live_{secrets.token_hex(16)}"
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO api_keys (key_token, user_name, is_active) VALUES (?, ?, 1)",
                (token, user_name.strip())
            )
            conn.commit()
        return token

    def validate_key(self, token: str) -> bool:
        """ตรวจสอบว่ากุญแจถูกต้องและยังไม่ถูก Revoke หรือไม่"""
        if not token:
            return False
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT id FROM api_keys WHERE key_token = ? AND is_active = 1",
                (token.strip(),)
            ).fetchone()
            return row is not None

    def revoke_key(self, key_id: int) -> bool:
        """สั่งเพิกถอนกุญแจทันที"""
        with self._get_connection() as conn:
            cur = conn.execute(
                "UPDATE api_keys SET is_active = 0, revoked_at = ? WHERE id = ?",
                (datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"), key_id)
            )
            conn.commit()
            return cur.rowcount > 0

    def list_keys(self) -> list[dict]:
        """ดึงรายการกุญแจทั้งหมดสำหรับแสดงบนหน้าเว็บ Admin"""
        with self._get_connection() as conn:
            rows = conn.execute(
                "SELECT id, key_token, user_name, is_active, created_at, revoked_at FROM api_keys ORDER BY id DESC"
            ).fetchall()
            return [dict(r) for r in rows]

    def get_cached_response(self, query_text: str) -> list[str] | None:
        """ค้นหาผลลัพธ์ในแคชจาก SHA-256 ของคำถามที่ผ่าน Normalize (ลด Latency จาก 8s เหลือ <5ms)"""
        query_norm = " ".join(query_text.strip().lower().split())
        query_hash = hashlib.sha256(query_norm.encode("utf-8")).hexdigest()
        with self._get_connection() as conn:
            row = conn.execute(
                "SELECT cached_events FROM legal_cache WHERE query_hash = ? AND expires_at > CURRENT_TIMESTAMP",
                (query_hash,)
            ).fetchone()
            if row:
                return json.loads(row["cached_events"])
        return None

    def set_cached_response(self, query_text: str, events: list[str], ttl_hours: int = 24):
        """บันทึก SSE events ทั้งหมดลงแคช พร้อมกำหนดเวลาหมดอายุ (TTL)"""
        query_norm = " ".join(query_text.strip().lower().split())
        query_hash = hashlib.sha256(query_norm.encode("utf-8")).hexdigest()
        expires_at = (datetime.now(timezone.utc) + timedelta(hours=ttl_hours)).strftime("%Y-%m-%d %H:%M:%S")
        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO legal_cache (query_hash, query_text, cached_events, expires_at)
                VALUES (?, ?, ?, ?)
            """, (query_hash, query_text, json.dumps(events, ensure_ascii=False), expires_at))
            conn.commit()

    def purge_expired_cache(self) -> int:
        """ล้างรายการแคชที่หมดอายุ (Auto Purge) เพื่อรักษาขนาดฐานข้อมูล keys.db ให้กะทัดรัดเสมอ"""
        with self._get_connection() as conn:
            cur = conn.execute("DELETE FROM legal_cache WHERE expires_at <= CURRENT_TIMESTAMP")
            conn.commit()
            return cur.rowcount