"""Structured audit logging for EAxCRM generator/sync scripts.

Provides ChangeLog (a per-run audit trail writer) and compute_md_diff (a
module-level function for comparing two process-MD texts).
"""

import os
import re
import datetime


def compute_md_diff(old_content: str, new_content: str) -> dict:
    """Compare two process MD texts and return a structured diff dict.

    Args:
        old_content: Previous Markdown content (or empty string).
        new_content: New Markdown content.

    Returns:
        A dict with keys "created", "deleted", "updated", "connectors".
        Each maps to a list of dicts suitable for ChangeLog.log_diff().
    """

    def extract_elements(text):
        elems = {}
        for line in text.splitlines():
            m = re.match(r"#{2,4}\s+(.+?)[\u2014\u2013]\s*(.+)", line)
            if m:
                label = m.group(1).strip()
                eid = m.group(2).strip()
                elems[eid] = {"type": label}
        return elems

    old_elems = extract_elements(old_content) if old_content else {}
    new_elems = extract_elements(new_content)

    old_ids = set(old_elems.keys())
    new_ids = set(new_elems.keys())

    diff = {
        "created": [
            {"eid": eid, "name": eid, "type": new_elems[eid]["type"]}
            for eid in sorted(new_ids - old_ids)
        ],
        "deleted": [
            {"eid": eid, "name": eid, "type": old_elems[eid]["type"]}
            for eid in sorted(old_ids - new_ids)
        ],
        "updated": [],
        "connectors": [],
    }
    for eid in sorted(old_ids & new_ids):
        old_t = old_elems[eid]["type"]
        new_t = new_elems[eid]["type"]
        if old_t != new_t:
            diff["updated"].append(
                {
                    "eid": eid,
                    "name": eid,
                    "type": new_t,
                    "changes": {"Type": (old_t, new_t)},
                }
            )

    def extract_connectors(text):
        conns = set()
        in_conn_section = False
        for line in text.splitlines():
            if re.match(r"##\s+(Sequence|Message|Data)", line):
                in_conn_section = True
                continue
            if line.startswith("## "):
                in_conn_section = False
                continue
            if in_conn_section and line.startswith("- "):
                m = re.match(
                    r"(.+?)\s*[\u2192\u279e]\s*(.+?)(?:\s*\[(.+?)\])?$",
                    line[2:],
                )
                if m:
                    conns.add((m.group(1).strip(), m.group(2).strip()))
        return conns

    old_conns = extract_connectors(old_content) if old_content else set()
    new_conns = extract_connectors(new_content)

    for src, tgt in sorted(new_conns - old_conns):
        diff["connectors"].append(
            {
                "action": "created",
                "type": "connector",
                "source": src,
                "target": tgt,
                "condition": "",
            }
        )
    for src, tgt in sorted(old_conns - new_conns):
        diff["connectors"].append(
            {
                "action": "deleted",
                "type": "connector",
                "source": src,
                "target": tgt,
                "condition": "",
            }
        )

    return diff


class ChangeLog:
    """Per-run audit trail that accumulates entries and writes Markdown.

    Usage::

        clog = ChangeLog("changelog.md")
        clog.checkpoint("Parsed MD")
        clog.log("created", "CreateRFQ", "Create RFQ", "Activity")
        clog.log_diff(some_diff_dict)
        clog.close()          # writes prepended section, trims if oversize
    """

    def __init__(self, filepath: str, max_bytes: int = 1_000_000):
        self.filepath = filepath
        self.max_bytes = max_bytes
        self._entries: list[dict] = []
        self._checkpoints: list[dict] = []

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def log(
        self,
        action: str,
        eid: str,
        name: str,
        kind: str,
        guid: str = "",
        changes: dict | None = None,
        run_id: str = "",
    ) -> None:
        """Record a single action (created / updated / deleted / conn_*).

        Args:
            action: ``"created"``, ``"updated"``, ``"deleted"``,
                ``"conn_created"``, or ``"conn_deleted"``.
            eid: Element identifier (for connectors: the connector type).
            name: Human-readable name (for connectors: source element).
            kind: BPMN/ArchiMate type (for connectors: target element).
            guid: EA GUID (optional).
            changes: Dict of {field: (old, new)} for ``"updated"`` entries,
                or ``{"condition": ..., ...}`` for connectors.
            run_id: Optional run identifier.
        """
        self._entries.append(
            {
                "action": action,
                "eid": eid,
                "name": name,
                "type": kind,
                "guid": guid,
                "changes": changes or {},
                "run_id": run_id,
            }
        )

    def checkpoint(self, phase: str, run_id: str = "") -> None:
        """Record a checkpoint / phase name for this run."""
        self._checkpoints.append({"phase": phase, "run_id": run_id})

    def log_diff(self, diff: dict, run_id: str = "") -> None:
        """Process a structured diff dict (as returned by compute_md_diff).

        Calls ``log()`` for each item in the diff's sub-lists.
        """
        for item in diff.get("created", []):
            self.log(
                "created",
                item["eid"],
                item.get("name", item["eid"]),
                item.get("type", ""),
                run_id=run_id,
            )
        for item in diff.get("deleted", []):
            self.log(
                "deleted",
                item["eid"],
                item.get("name", item["eid"]),
                item.get("type", ""),
                run_id=run_id,
            )
        for item in diff.get("updated", []):
            self.log(
                "updated",
                item["eid"],
                item.get("name", item["eid"]),
                item.get("type", ""),
                changes=item.get("changes", {}),
                run_id=run_id,
            )
        for item in diff.get("connectors", []):
            self.log(
                "conn_" + item["action"],
                item.get("type", ""),
                item.get("source", ""),
                item.get("target", ""),
                changes={"condition": item.get("condition", "")},
                run_id=run_id,
            )

    def close(self) -> None:
        """Finalise the current run and prepend it to the file.

        - If no entries or checkpoints have been recorded, does nothing.
        - Reads the existing file, prepends the new ``##`` section.
        - If the combined content exceeds ``max_bytes``, removes oldest
          ``##`` sections from the end until it fits (always keeps at
          least one section).
        """
        if not self._entries and not self._checkpoints:
            return

        section = self._format_section()

        existing = ""
        if os.path.exists(self.filepath):
            with open(self.filepath, "r", encoding="utf-8") as f:
                existing = f.read()

        content = section + existing

        # Trim oldest sections if over the size limit.
        if len(content.encode("utf-8")) > self.max_bytes:
            content = self._trim_oldest(content)

        with open(self.filepath, "w", encoding="utf-8") as f:
            f.write(content)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _format_section(self) -> str:
        """Build the Markdown ``##`` section for the current buffer."""
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Collect unique run_ids
        run_ids: set[str] = set()
        for e in self._entries:
            if e["run_id"]:
                run_ids.add(e["run_id"])
        for c in self._checkpoints:
            if c["run_id"]:
                run_ids.add(c["run_id"])
        run_id_str = f", run {next(iter(run_ids))}" if run_ids else ""

        lines = [f"## {now} — Audit{run_id_str}\n"]

        # -- Checkpoints ---------------------------------------------------
        if self._checkpoints:
            lines.append("\n### Checkpoints\n")
            for cp in self._checkpoints:
                lines.append(f"- {cp['phase']}\n")

        # Group entries by action
        created = [e for e in self._entries if e["action"] == "created"]
        updated = [e for e in self._entries if e["action"] == "updated"]
        deleted = [e for e in self._entries if e["action"] == "deleted"]
        connectors = [e for e in self._entries if e["action"].startswith("conn_")]

        # -- Created -------------------------------------------------------
        if created:
            lines.append("\n### Created\n")
            lines.append("| eid | Name | Type | GUID |\n")
            lines.append("|-----|------|------|------|\n")
            for e in created:
                lines.append(
                    f"| {e['eid']} | {e['name']} | {e['type']} | {e['guid']} |\n"
                )

        # -- Updated -------------------------------------------------------
        if updated:
            lines.append("\n### Updated\n")
            lines.append("| eid | Name | Type | GUID | Changes |\n")
            lines.append("|-----|------|------|------|---------|\n")
            for e in updated:
                changes_parts = []
                for k, v in e.get("changes", {}).items():
                    old_val, new_val = v
                    changes_parts.append(f"{k}: {old_val} -> {new_val}")
                changes_str = "; ".join(changes_parts)
                lines.append(
                    f"| {e['eid']} | {e['name']} | {e['type']} | "
                    f"{e['guid']} | {changes_str} |\n"
                )

        # -- Deleted -------------------------------------------------------
        if deleted:
            lines.append("\n### Deleted\n")
            lines.append("| eid | Name | Type | GUID |\n")
            lines.append("|-----|------|------|------|\n")
            for e in deleted:
                lines.append(
                    f"| {e['eid']} | {e['name']} | {e['type']} | {e['guid']} |\n"
                )

        # -- Connectors ----------------------------------------------------
        if connectors:
            lines.append("\n### Connectors\n")
            lines.append("| Action | Type | Source | Target | Condition |\n")
            lines.append("|--------|------|--------|--------|-----------|\n")
            for e in connectors:
                bare_action = e["action"].replace("conn_", "")
                cond = e.get("changes", {}).get("condition", "")
                lines.append(
                    f"| {bare_action} | {e['eid']} | {e['name']} | "
                    f"{e['type']} | {cond} |\n"
                )

        lines.append("\n")
        return "".join(lines)

    def _trim_oldest(self, content: str) -> str:
        """Remove oldest ``##`` sections until content fits ``max_bytes``.

        Always keeps at least one section.
        """
        # Split on section boundaries: newline followed by "## "
        sections = re.split(r"\n(?=## )", content)
        while (
            len(sections) > 1
            and len("".join(sections).encode("utf-8")) > self.max_bytes
        ):
            sections.pop()  # Remove the oldest (last) section
        return "".join(sections)
