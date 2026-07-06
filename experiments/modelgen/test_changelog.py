"""Tests for changelog module."""
import os
import re
import tempfile
from pathlib import Path

import pytest

from changelog import ChangeLog, compute_md_diff


# =============================================================================
# Tests for compute_md_diff
# =============================================================================

OLD_TEXT = """## Elements

### Activity—CreateRFQ
- Name: Create RFQ
- Lane: Customer
- Notes: Creates a Request For Quote from a customer

### Activity—AcceptOffer
- Name: Accept Offer
- Lane: EAxpertise
- Notes: Customer accepts the offer

## Relationships

### SequenceFlow—sf1
- Source: CreateRFQ
- Target: AcceptOffer
- Name: Send quote
"""

NEW_TEXT = """## Elements

### Activity—CreateRFQ
- Name: Create RFQ
- Lane: Customer

### Gateway—duplicateCheck
- Name: Check duplicates
- Lane: EAxpertise

## Relationships

### SequenceFlow—sf1
- Source: CreateRFQ
- Target: duplicateCheck
- Name: Send data
"""


def test_compute_md_diff_created_deleted():
    """Detect newly created and deleted elements."""
    diff = compute_md_diff(OLD_TEXT, NEW_TEXT)
    assert "created" in diff
    created_ids = [e["eid"] for e in diff["created"]]
    assert "duplicateCheck" in created_ids, (
        f"Expected duplicateCheck in created, got {created_ids}"
    )
    assert "deleted" in diff
    deleted_ids = [e["eid"] for e in diff["deleted"]]
    assert "AcceptOffer" in deleted_ids, (
        f"Expected AcceptOffer in deleted, got {deleted_ids}"
    )


def test_compute_md_diff_updated():
    """Detect type changes between BPMN types."""
    old = "### Activity—AcceptOffer\n- Name: Accept Offer\n"
    new = "### Gateway—AcceptOffer\n- Name: Accept Offer\n"
    diff = compute_md_diff(old, new)
    assert len(diff["updated"]) == 1
    assert diff["updated"][0]["eid"] == "AcceptOffer"
    assert diff["updated"][0]["changes"]["Type"] == ("Activity", "Gateway")


def test_compute_md_diff_empty_old():
    """All elements in new are created when old is empty.

    Note: the element regex matches ALL ``#`` headers with an em-dash,
    including ``### SequenceFlow---sf1`` under Relationships, not only
    the Elements section.
    """
    diff = compute_md_diff("", NEW_TEXT)
    # CreateRFQ, duplicateCheck, _and_ the SequenceFlow sf1 header
    assert len(diff["created"]) == 3
    created_ids = {e["eid"] for e in diff["created"]}
    assert "CreateRFQ" in created_ids
    assert "duplicateCheck" in created_ids
    assert len(diff["deleted"]) == 0
    assert len(diff["updated"]) == 0


def test_compute_md_diff_empty_new():
    """All elements in old are deleted when new is empty."""
    diff = compute_md_diff(OLD_TEXT, "")
    assert len(diff["deleted"]) == 3  # CreateRFQ, AcceptOffer, sf1
    deleted_ids = {e["eid"] for e in diff["deleted"]}
    assert "CreateRFQ" in deleted_ids
    assert "AcceptOffer" in deleted_ids
    assert len(diff["created"]) == 0


def test_compute_md_diff_no_changes():
    """No diffs when content is identical."""
    diff = compute_md_diff(OLD_TEXT, OLD_TEXT)
    assert len(diff["created"]) == 0
    assert len(diff["deleted"]) == 0
    assert len(diff["updated"]) == 0
    assert len(diff["connectors"]) == 0


# =============================================================================
# Tests for ChangeLog class
# =============================================================================


@pytest.fixture
def clog_path():
    """Yield a clean temporary file path, then clean up."""
    tmp = tempfile.NamedTemporaryFile(suffix=".md", delete=True)
    path = tmp.name
    tmp.close()  # file is deleted because delete=True
    yield path
    if os.path.exists(path):
        os.unlink(path)


def test_log_creates_file(clog_path):
    """Logging then close() creates the file on disk."""
    clog = ChangeLog(clog_path)
    clog.log("created", "CreateRFQ", "Create RFQ", "Activity")
    clog.close()
    assert os.path.exists(clog_path), "File should exist after close()"
    content = Path(clog_path).read_text(encoding="utf-8")
    assert "CreateRFQ" in content
    assert "### Created" in content
    assert "### Deleted" not in content


def test_prepend_newest_first(clog_path):
    """Newest run is prepended (appears first in the file)."""
    # First run
    cl = ChangeLog(clog_path)
    cl.log("created", "First", "First", "Activity")
    cl.close()

    # Second run
    cl2 = ChangeLog(clog_path)
    cl2.log("created", "Second", "Second", "Activity")
    cl2.close()

    content = Path(clog_path).read_text(encoding="utf-8")
    # The first section after --- or file start should contain "Second"
    sections = re.split(r"\n(?=## )", content)
    first_section = sections[0]
    assert "Second" in first_section, (
        f"Newest entry 'Second' should appear first. Sections: "
        f"{[s[:60] for s in sections]}"
    )


def test_log_updated_with_changes(clog_path):
    """Updated entries render Changes column correctly."""
    clog = ChangeLog(clog_path)
    clog.log(
        "updated", "AcceptOffer", "Accept Offer", "Activity",
        changes={"Notes": ("old note", "new note")},
    )
    clog.close()
    content = Path(clog_path).read_text(encoding="utf-8")
    assert "### Updated" in content
    assert "AcceptOffer" in content
    assert "old note ->" in content
    assert "new note" in content


def test_log_pure_name_change_is_renamed_not_updated(clog_path):
    """An 'updated' log whose only change is Name is reclassified to its
    own Renamed section, not folded into Updated."""
    clog = ChangeLog(clog_path)
    clog.log(
        "updated", "AcceptOffer", "Accept Offer", "Activity",
        changes={"Name": ("Accept", "Accept Offer")},
    )
    clog.close()
    content = Path(clog_path).read_text(encoding="utf-8")
    assert "### Renamed" in content
    assert "### Updated" not in content
    assert "AcceptOffer" in content
    assert "Accept -> Accept Offer" in content


def test_log_name_plus_other_change_stays_updated(clog_path):
    """A Name change alongside another field change is NOT a pure rename --
    it stays under Updated, with Name still shown in the Changes column."""
    clog = ChangeLog(clog_path)
    clog.log(
        "updated", "AcceptOffer", "Accept Offer", "Activity",
        changes={"Name": ("Accept", "Accept Offer"), "Notes": ("old", "new")},
    )
    clog.close()
    content = Path(clog_path).read_text(encoding="utf-8")
    assert "### Updated" in content
    assert "### Renamed" not in content
    assert "Accept -> Accept Offer" in content


def test_log_diff_detects_rename(clog_path):
    """compute_md_diff picks up a Name-only change from the MD's '- Name:'
    field and routes it through the same rename reclassification."""
    old_md = "### Activity—CreateAccount\n- Name: Create Account\n- Type: Activity\n"
    new_md = "### Activity—CreateAccount\n- Name: Create Customer Account\n- Type: Activity\n"
    diff = compute_md_diff(old_md, new_md)
    clog = ChangeLog(clog_path)
    clog.log_diff(diff)
    clog.close()
    content = Path(clog_path).read_text(encoding="utf-8")
    assert "### Renamed" in content
    assert "Create Account -> Create Customer Account" in content


def test_log_deleted(clog_path):
    """Deleted entries appear in Deleted section."""
    clog = ChangeLog(clog_path)
    clog.log("deleted", "OldElem", "Old Element", "DataObject")
    clog.close()
    content = Path(clog_path).read_text(encoding="utf-8")
    assert "### Deleted" in content
    assert "OldElem" in content
    assert "Old Element" in content


def test_size_cap_trims_oldest(clog_path):
    """When file exceeds max_bytes, oldest sections are removed."""
    # Write many entries with a small max_bytes
    for i in range(25):
        c = ChangeLog(clog_path, max_bytes=500)
        c.log("created", f"Elem{i}", f"Elem{i}", "Activity")
        c.close()

    content = Path(clog_path).read_text(encoding="utf-8")
    # File should be bounded (500 + some margin for the encoding difference)
    assert os.path.getsize(clog_path) <= 700, (
        f"File size {os.path.getsize(clog_path)} exceeds 700"
    )
    # Evidence of trimming: not all 25 sections are present
    section_count = content.count("### Created")
    assert section_count < 25, (
        f"Expected fewer than 25 sections after trim, got {section_count}"
    )
    # The most recent entries should survive, oldest may be gone
    assert "Elem24" in content, "Most recent entry should survive trimming"
    assert "Elem0" not in content or section_count < 25, (
        "Oldest entries may have been trimmed"
    )


def test_checkpoint(clog_path):
    """Checkpoints appear in the Checkpoints section."""
    clog = ChangeLog(clog_path)
    clog.checkpoint("Parsed MD")
    clog.checkpoint("Elements complete")
    clog.log("created", "X", "X", "Activity")
    clog.close()
    content = Path(clog_path).read_text(encoding="utf-8")
    assert "### Checkpoints" in content
    assert "- Parsed MD" in content
    assert "- Elements complete" in content


def test_log_diff_created_deleted(clog_path):
    """log_diff processes a diff dict into entries."""
    clog = ChangeLog(clog_path)
    diff = {
        "created": [
            {"eid": "NewElem", "name": "New Elem", "type": "Activity"},
        ],
        "deleted": [
            {"eid": "OldElem", "name": "Old Elem", "type": "DataObject"},
        ],
        "updated": [],
        "connectors": [
            {
                "action": "created",
                "type": "SequenceFlow",
                "source": "A",
                "target": "B",
                "condition": "",
            },
        ],
    }
    clog.log_diff(diff)
    clog.close()
    content = Path(clog_path).read_text(encoding="utf-8")
    assert "NewElem" in content, "Created element should appear"
    assert "OldElem" in content, "Deleted element should appear"
    assert "### Connectors" in content, "Connectors section should exist"
    assert "SequenceFlow" in content, "Connector type should appear"


def test_empty_buffer_no_file(clog_path):
    """close() with no entries does not create a file."""
    clog = ChangeLog(clog_path)
    clog.close()
    assert not os.path.exists(clog_path), (
        "File should not be created with no entries"
    )


def test_log_deleted_no_guid(clog_path):
    """Deleted entries without a GUID still render cleanly."""
    clog = ChangeLog(clog_path)
    clog.log("deleted", "Orphan", "Orphan Element", "Artifact")
    clog.close()
    content = Path(clog_path).read_text(encoding="utf-8")
    assert "Orphan" in content
    assert "Artifact" in content


def test_multiple_same_run_id(clog_path):
    """Multiple entries with the same run_id produce one header."""
    clog = ChangeLog(clog_path)
    clog.log("created", "A", "A", "Activity", run_id="run-001")
    clog.log("created", "B", "B", "Activity", run_id="run-001")
    clog.close()
    content = Path(clog_path).read_text(encoding="utf-8")
    # The run_id should appear once in the header
    assert content.count("run-001") >= 1
    assert "A" in content
    assert "B" in content


def test_unicode_changes_display(clog_path):
    """Changes with unicode arrows or special chars render."""
    clog = ChangeLog(clog_path)
    clog.log(
        "updated", "Elem", "Elem", "Activity",
        changes={"Name": ("old name", "new name")},
    )
    clog.close()
    content = Path(clog_path).read_text(encoding="utf-8")
    assert "old name" in content
    assert "new name" in content


def test_multiple_connectors_logged(clog_path):
    """Multiple connectors in log_diff all appear."""
    clog = ChangeLog(clog_path)
    diff = {
        "created": [],
        "deleted": [],
        "updated": [],
        "connectors": [
            {
                "action": "created",
                "type": "SequenceFlow",
                "source": "A",
                "target": "B",
                "condition": "if true",
            },
            {
                "action": "deleted",
                "type": "MessageFlow",
                "source": "C",
                "target": "D",
                "condition": "",
            },
        ],
    }
    clog.log_diff(diff)
    clog.close()
    content = Path(clog_path).read_text(encoding="utf-8")
    assert "A" in content
    assert "B" in content
    assert "C" in content
    assert "D" in content
    assert "if true" in content
