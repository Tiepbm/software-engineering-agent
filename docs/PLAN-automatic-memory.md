# Plan: Automatic Memory cho CE7 Agent

**Status:** Draft — chưa implement
**Created:** 2026-04-28
**Author:** Kiro + User
**Priority:** P2 (implement sau khi có real usage data)

---

## 1. Mục tiêu

Agent tự động lưu và truy vấn lịch sử tương tác mà không cần user trigger:
- Tự ghi sau mỗi interaction (packs used, quality, routing correctness)
- Tự truy vấn trước khi routing (tìm patterns từ lịch sử)
- Tự tổng hợp patterns theo thời gian
- Chạy local, zero cost, portable

## 2. Quyết định: MCP Memory Server (Option A)

| Option | Đánh giá | Chọn? |
|---|---|---|
| A. MCP Server (SQLite) | Semantic search, structured, auto, cross-session | ✅ Chọn |
| B. File-based + Hooks | Đơn giản nhưng không search, chỉ Kiro | ❌ |
| C. Hybrid (MCP + file export) | Best of both nhưng phức tạp nhất | Partial — Phase 3 |

Lý do chọn A:
- Kiro hỗ trợ MCP sẵn
- SQLite = zero cost, local, portable
- FTS5 đủ cho ~1000 interactions
- Một khi setup xong, hoàn toàn tự động

## 3. Kiến trúc

```
User prompt
  → Agent gọi search_memory("payment idempotency")
  → MCP server trả về: relevant past interactions
  → Agent routing + trả lời (informed by memory)
  → Agent gọi save_interaction({summary, packs, quality})
  → MCP server lưu vào SQLite
```

### Storage

```
~/.ce7/memory.db (SQLite)
  ├── interactions     ← mỗi câu hỏi + routing decision + quality
  ├── patterns         ← auto-synthesized từ interactions
  └── corrections      ← routing mistakes + root cause
```

### MCP Tools

| Tool | Input | Output | Khi nào |
|---|---|---|---|
| `search_memory` | query, limit | Past interactions matching query | Trước routing |
| `save_interaction` | prompt_summary, domain, risk_class, packs, refs, quality | {id, saved} | Sau trả lời |
| `save_correction` | prompt_summary, expected_packs, actual_packs, root_cause | {id, saved} | Khi routing sai |
| `get_patterns` | domain? | Top patterns by frequency | Trước routing |
| `get_stats` | none | Total interactions, accuracy, top domains | On demand |
| `export_patterns` | output_path | Writes learned-patterns.md | Periodic |

### Search strategy

Phase 1: SQLite FTS5 (keyword matching) — đủ cho ~1000 interactions.
Phase 4 (future): Vector embeddings nếu FTS5 không đủ.

## 4. Files cần tạo

```
software-engineering-agent/
  mcp-memory/
    server.py              ← MCP server (~200 lines Python)
    schema.sql             ← SQLite schema (3 tables)
    requirements.txt       ← mcp library
    README.md              ← Setup + usage guide
```

### SQLite Schema (draft)

```sql
CREATE VIRTUAL TABLE interactions_fts USING fts5(prompt_summary, domain);

CREATE TABLE interactions (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp       TEXT NOT NULL DEFAULT (datetime('now')),
  prompt_summary  TEXT NOT NULL,
  domain          TEXT,
  risk_class      TEXT,
  packs_activated TEXT NOT NULL,  -- JSON array
  references_used TEXT NOT NULL,  -- JSON array
  quality         TEXT NOT NULL,  -- good | acceptable | poor
  feedback        TEXT,
  routing_correct INTEGER NOT NULL DEFAULT 1,  -- 1=true, 0=false
  notes           TEXT
);

CREATE TABLE patterns (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  pattern_text    TEXT NOT NULL,
  frequency       INTEGER NOT NULL DEFAULT 1,
  last_seen       TEXT NOT NULL DEFAULT (datetime('now')),
  confidence      REAL NOT NULL DEFAULT 0.5,
  domain          TEXT,
  source          TEXT NOT NULL DEFAULT 'auto'  -- auto | manual
);

CREATE TABLE corrections (
  id              INTEGER PRIMARY KEY AUTOINCREMENT,
  timestamp       TEXT NOT NULL DEFAULT (datetime('now')),
  prompt_summary  TEXT NOT NULL,
  expected_packs  TEXT NOT NULL,  -- JSON array
  actual_packs    TEXT NOT NULL,  -- JSON array
  root_cause      TEXT NOT NULL,
  fixed           INTEGER NOT NULL DEFAULT 0
);
```

## 5. Agent Integration

### copilot-instructions.md (update)

```markdown
## Memory (MCP)
- Before routing: call `search_memory` with short summary of user's question.
  If relevant past interactions found, use them to inform pack selection.
- After answering: call `save_interaction` with prompt summary, packs, refs, quality.
- If user indicates routing was wrong: call `save_correction`.
- Do NOT block on memory failures — if MCP unavailable, proceed without memory.
```

### Fallback

Nếu MCP server không available (Copilot chưa hỗ trợ MCP):
- Agent fallback đọc `memory/learned-patterns.md` (file-based, đã có)
- `export_patterns` tool xuất từ SQLite ra file này

## 6. Platform Config

| Platform | Config file | MCP support |
|---|---|---|
| Kiro | `.kiro/settings/mcp.json` | ✅ Native |
| Claude Code | `.mcp.json` | ✅ Native |
| Copilot | Chưa có | ❌ Fallback to file |

### Kiro config (draft)

```json
{
  "mcpServers": {
    "ce7-memory": {
      "command": "python3",
      "args": ["mcp-memory/server.py"],
      "env": {
        "CE7_MEMORY_DB": "~/.ce7/memory.db"
      }
    }
  }
}
```

## 7. Implementation Phases

| Phase | Nội dung | Effort | Prerequisite |
|---|---|---|---|
| **Phase 1** | MCP server + SQLite + 5 tools + Kiro config | 1 session | Python 3.10+, `mcp` library |
| **Phase 2** | Auto-synthesize patterns (mỗi 20 interactions) | Nhỏ | 20+ real interactions |
| **Phase 3** | Export `learned-patterns.md` tự động (Copilot fallback) | Nhỏ | Phase 2 |
| **Phase 4** | Vector embeddings cho semantic search | Trung bình | 500+ interactions, nếu FTS5 không đủ |

## 8. Acceptance Criteria

### Phase 1 done khi:
- [ ] `python3 mcp-memory/server.py` starts without error
- [ ] Kiro can call `save_interaction` and `search_memory` via MCP
- [ ] Data persists in `~/.ce7/memory.db` across sessions
- [ ] Agent instructions updated to call memory tools
- [ ] Fallback to file-based memory works when MCP unavailable

### Phase 2 done khi:
- [ ] After 20 interactions, `get_patterns` returns auto-synthesized patterns
- [ ] Patterns include frequency and confidence scores
- [ ] Patterns are domain-aware (banking vs insurance vs cross-domain)

## 9. Risks và Mitigations

| Risk | Mitigation |
|---|---|
| MCP server crashes | Agent has fallback to file-based memory; never blocks on memory failure |
| SQLite grows too large | Auto-archive interactions older than 6 months; keep patterns indefinitely |
| FTS5 search quality poor | Phase 4 adds vector embeddings; until then, keyword search is sufficient |
| Copilot doesn't support MCP | File-based fallback via `export_patterns` → `learned-patterns.md` |
| Memory contains wrong patterns | `corrections` table tracks mistakes; patterns auto-adjust confidence |

## 10. Không làm

- Không dùng external database (PostgreSQL, Redis) — SQLite đủ
- Không dùng cloud storage — local only, privacy first
- Không dùng vector embeddings ở Phase 1 — FTS5 đủ cho scale hiện tại
- Không auto-modify agent/skill files dựa trên memory — chỉ inform routing decisions
- Không lưu full prompt/response — chỉ summary + metadata (token efficient)
