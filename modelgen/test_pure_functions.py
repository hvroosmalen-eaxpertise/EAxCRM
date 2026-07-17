"""Pure Python tests for modelgen functions (no EA COM API required).

These tests run on any platform and cover the layout math, MD parsing, path
routing, and graph algorithms that previously had no automated checks.
"""
import os
import tempfile
import textwrap

import pytest

from bpmn_engine import safe_id, get_lane_from_fields, _parse_md_flat, _parse_md_hierarchical
from bpmn_engine import _connector_path, _message_flow_path
from bpmn_engine import _bottom_right_positions_for_new
from bpmn_config import LABEL_TO_STEREO, OBJECT_TYPE_MAP, BPMN_TAGGED_VALUES
from bpmn_config import CONNECTOR_TYPES, CONNECTOR_STEREOTYPE_EX
from diagram_utils import (
    compute_bpmn_lane_positions,
    compute_bpmn_element_positions,
    compute_bpmn_flow_layout,
    compute_diagonal_positions,
    compute_grid_positions,
    compute_uml_class_height,
    compute_uml_class_width,
    sort_by_flow_order,
    find_longest_path,
    BPMN_ELEMENT_SIZES,
)


# ===========================================================================
# safe_id
# ===========================================================================


class TestSafeId:
    def test_simple(self):
        assert safe_id("HelloWorld") == "HelloWorld"

    def test_lowercase(self):
        assert safe_id("helloWorld") == "helloWorld"

    def test_strips_special_chars(self):
        # safe_id keeps only a-zA-Z0-9
        assert safe_id("Hello World!") == "HelloWorld"

    def test_numbers(self):
        assert safe_id("elem42") == "elem42"

    def test_underscores_stripped(self):
        assert safe_id("hello_world") == "helloworld"

    def test_dashes_stripped(self):
        assert safe_id("hello-world") == "helloworld"

    def test_empty_string(self):
        assert safe_id("") == ""

    def test_only_special_chars(self):
        assert safe_id("!@#$%") == ""


# ===========================================================================
# get_lane_from_fields
# ===========================================================================


class TestGetLaneFromFields:
    def test_lane_key(self):
        assert get_lane_from_fields({"Lane": "Customer"}) == "Customer"

    def test_lane_lowercase(self):
        assert get_lane_from_fields({"lane": "eAxpertise"}) == "eAxpertise"

    def test_lane_takes_precedence(self):
        assert get_lane_from_fields(
            {"Lane": "Customer", "Parent": "SomeLane"}
        ) == "Customer"

    def test_parent_fallback(self):
        assert get_lane_from_fields({"Parent": "SomeParent"}) == "SomeParent"

    def test_none_fields(self):
        assert get_lane_from_fields(None) is None

    def test_empty_fields(self):
        assert get_lane_from_fields({}) is None

    def test_no_relevant_keys(self):
        assert get_lane_from_fields({"Name": "foo"}) is None


# ===========================================================================
# compute_bpmn_lane_positions
# ===========================================================================


class TestComputeBpmnLanePositions:
    def test_single_lane(self):
        lanes = [{"id": "lane1"}]
        result = compute_bpmn_lane_positions(lanes)
        assert "lane1" in result
        l, t, r, b = result["lane1"]
        assert l == 0
        assert t == 30
        assert r == 1000
        assert b == 530  # 30 + 500

    def test_two_lanes_with_gap(self):
        lanes = [{"id": "l1"}, {"id": "l2"}]
        result = compute_bpmn_lane_positions(lanes, lane_height=200, gap=50)
        l1 = result["l1"]  # (0, 30, 1000, 230)
        l2 = result["l2"]  # (0, 480, 1000, 680) = 230 + 250(gap) ... wait
        # 30 + 200 = 230, + 50 gap = 280 start for l2, + 200 = 480
        assert l1 == (0, 30, 1000, 230)
        assert l2 == (0, 280, 1000, 480)

    def test_custom_width(self):
        lanes = [{"id": "lane1"}]
        result = compute_bpmn_lane_positions(lanes, lane_width=800)
        assert result["lane1"][2] == 800


# ===========================================================================
# compute_bpmn_element_positions (grid-within-lane)
# ===========================================================================


class TestComputeBpmnElementPositions:
    def test_single_element(self):
        bounds = {"lane1": (0, 30, 1000, 530)}
        elements = {"lane1": ["e1"]}
        result = compute_bpmn_element_positions(elements, bounds)
        assert "e1" in result
        x, y, r, b = result["e1"]
        assert x >= 0
        assert y >= 0
        assert r > x
        assert b > y

    def test_two_elements_same_lane(self):
        bounds = {"lane1": (0, 30, 1000, 530)}
        elements = {"lane1": ["e1", "e2"]}
        result = compute_bpmn_element_positions(elements, bounds)
        assert "e1" in result and "e2" in result
        # e2 should be to the right of e1
        assert result["e1"][0] < result["e2"][0]

    def test_elements_per_lane(self):
        bounds = {"l1": (0, 30, 1000, 530), "l2": (0, 580, 1000, 1080)}
        elements = {"l1": ["e1"], "l2": ["e2"]}
        result = compute_bpmn_element_positions(elements, bounds)
        # Different lanes, so e2 should be below e1
        assert result["e1"][1] < result["e2"][1]

    def test_elem_types_sizing(self):
        bounds = {"lane1": (0, 30, 800, 530)}
        elements = {"lane1": ["e1"]}
        result = compute_bpmn_element_positions(
            elements, bounds, elem_types={"e1": "StartEvent"}
        )
        # StartEvent is 30x30
        x, y, r, b = result["e1"]
        assert (r - x) == 30
        assert (b - y) == 30

    def test_unknown_elem_type_falls_back(self):
        bounds = {"lane1": (0, 30, 800, 530)}
        elements = {"lane1": ["e1"]}
        result = compute_bpmn_element_positions(
            elements, bounds, elem_types={"e1": "NonExistentType"}
        )
        x, y, r, b = result["e1"]
        # Falls back to default 180x70
        assert (r - x) == 180
        assert (b - y) == 70


# ===========================================================================
# compute_diagonal_positions
# ===========================================================================


class TestComputeDiagonalPositions:
    def test_single_element(self):
        result = compute_diagonal_positions(["e1"])
        assert "e1" in result
        x, y, r, b = result["e1"]
        assert r - x == 180
        assert b - y == 120

    def test_elements_in_diagonal_staircase(self):
        result = compute_diagonal_positions(["e1", "e2"])
        e1x, e1y, _, _ = result["e1"]
        e2x, e2y, _, _ = result["e2"]
        # Default step=200, row_gap=200: e2 is diagonal offset
        assert e2x > e1x
        # Diagonal: same deltas for x and y
        assert (e2x - e1x) == (e2y - e1y)

    def test_with_start_index(self):
        result = compute_diagonal_positions(["e1"], start_index=5)
        x, y, _, _ = result["e1"]
        diag_pos = 5 % 8  # 5
        row = 5 // 8  # 0
        expected_x = 20 + diag_pos * 200  # 20 + 1000 = 1020
        expected_y = 20 + diag_pos * 200 + row * 200  # same
        assert x == expected_x
        assert y == expected_y


# ===========================================================================
# compute_grid_positions
# ===========================================================================


class TestComputeGridPositions:
    def test_single_element(self):
        result = compute_grid_positions(["e1"])
        assert "e1" in result
        x, y, r, b = result["e1"]
        assert r - x == 90
        assert b - y == 70

    def test_two_elements_side_by_side(self):
        result = compute_grid_positions(["e1", "e2"])
        assert result["e1"][0] < result["e2"][0]

    def test_elements_wrap_to_next_row(self):
        result = compute_grid_positions(
            ["e1", "e2", "e3", "e4", "e5", "e6", "e7", "e8", "e9"], per_row=8
        )
        # e9 should be in row 1 (below e1)
        assert result["e9"][1] > result["e1"][1]

    def test_with_sizes_dict(self):
        sizes = {"e1": (120, 80)}
        result = compute_grid_positions(["e1", "e2"], sizes=sizes)
        assert result["e1"][2] - result["e1"][0] == 120
        assert result["e1"][3] - result["e1"][1] == 80

    def test_with_elem_types_and_type_sizes(self):
        elem_types = {"e1": "Activity", "e2": "Component"}
        type_sizes = {"Activity": (110, 60), "Component": (90, 70)}
        result = compute_grid_positions(
            ["e1", "e2"], elem_types=elem_types, type_sizes=type_sizes
        )
        assert result["e1"][2] - result["e1"][0] == 110
        assert result["e1"][3] - result["e1"][1] == 60
        assert result["e2"][2] - result["e2"][0] == 90
        assert result["e2"][3] - result["e2"][1] == 70

    def test_sizes_takes_precedence(self):
        elem_types = {"e1": "Activity"}
        type_sizes = {"Activity": (110, 60)}
        sizes = {"e1": (200, 100)}
        result = compute_grid_positions(
            ["e1"], sizes=sizes, elem_types=elem_types, type_sizes=type_sizes
        )
        assert result["e1"][2] - result["e1"][0] == 200
        assert result["e1"][3] - result["e1"][1] == 100


# ===========================================================================
# compute_uml_class_height / width
# ===========================================================================


class TestComputeUmlClassHeight:
    def test_min_height(self):
        assert compute_uml_class_height(0) == 70  # min_height

    def test_small_attr_count(self):
        height = compute_uml_class_height(2)
        assert height == 70  # 30 + 2*16 + 6 = 68, min is 70

    def test_large_attr_count(self):
        height = compute_uml_class_height(10)
        assert height == 30 + 10 * 16 + 6  # 196

    def test_few_but_below_min(self):
        height = compute_uml_class_height(1)
        # 30 + 1*16 + 6 = 52, min 70
        assert height == 70

    def test_custom_params(self):
        height = compute_uml_class_height(3, header_height=20, row_height=12, min_height=50, padding=4)
        assert height == 20 + 3 * 12 + 4  # 60


class TestComputeUmlClassWidth:
    def test_min_width(self):
        assert compute_uml_class_width("A", []) == 120

    def test_long_name(self):
        name = "VeryLongClassName"
        width = compute_uml_class_width(name, [])
        # 16 chars * 5.5 + 10 = 98, but min 120
        assert width == 120

    def test_long_attr(self):
        name = "Short"
        attr_labels = ["some_very_long_attribute_name: string"]
        width = compute_uml_class_width(name, attr_labels)
        expected = len(attr_labels[0]) * 5.5 + 10
        assert width == pytest.approx(expected)

    def test_no_attr_labels(self):
        width = compute_uml_class_width("Foo", [], char_width=6, min_width=100, padding=20)
        # 3 * 6 + 20 = 38, min 100
        assert width == 100

    def test_longer_attr_wins_over_name(self):
        name = "Foo"
        attr_labels = ["abcdefghij" * 5]  # 50 chars
        width = compute_uml_class_width(name, attr_labels)
        expected = 50 * 5.5 + 10
        assert width == pytest.approx(expected)


# ===========================================================================
# sort_by_flow_order (DFS pre-order)
# ===========================================================================


class TestSortByFlowOrder:
    def test_single_element(self):
        result = sort_by_flow_order(["e1"], [])
        assert result == ["e1"]

    def test_linear_chain(self):
        flows = [{"source": "a", "target": "b"}, {"source": "b", "target": "c"}]
        result = sort_by_flow_order(["a", "b", "c"], flows)
        assert result.index("a") < result.index("b") < result.index("c")

    def test_data_objects_appended(self):
        flows = [{"source": "a", "target": "b"}]
        result = sort_by_flow_order(["a", "b", "d1", "d2"], flows)
        # 'a' and 'b' in flow order, 'd1'/'d2' appended at end
        assert result[:2] == ["a", "b"]
        assert result[2:] == ["d1", "d2"]

    def test_fork(self):
        flows = [
            {"source": "a", "target": "b"},
            {"source": "a", "target": "c"},
        ]
        result = sort_by_flow_order(["a", "b", "c"], flows)
        assert result[0] == "a"
        # b and c both after a
        assert result.index("b") > result.index("a")
        assert result.index("c") > result.index("a")

    def test_empty_lane(self):
        assert sort_by_flow_order([], []) == []

    def test_elements_not_in_flow(self):
        result = sort_by_flow_order(["x", "y", "z"], [])
        # All have no edges, so they go in original order
        assert result == ["x", "y", "z"]


# ===========================================================================
# find_longest_path
# ===========================================================================


class TestFindLongestPath:
    def test_single_edge(self):
        adj = {"a": ["b"]}
        result = find_longest_path(adj, ["a"])
        assert result == ["a", "b"]

    def test_chain(self):
        adj = {"a": ["b"], "b": ["c"]}
        result = find_longest_path(adj, ["a"])
        assert result == ["a", "b", "c"]

    def test_fork_longest_branch(self):
        adj = {"a": ["b", "c"], "b": ["d"], "c": [], "d": []}
        result = find_longest_path(adj, ["a"])
        # a -> b -> d (3) vs a -> c (2)
        assert result == ["a", "b", "d"]

    def test_no_start_nodes(self):
        assert find_longest_path({}, []) == []

    def test_cycle_handled(self):
        adj = {"a": ["b"], "b": ["a"]}
        result = find_longest_path(adj, ["a"])
        assert result == ["a", "b"]

    def test_disconnected_components(self):
        adj = {"a": ["b"], "b": [], "c": ["d"], "d": []}
        result = find_longest_path(adj, ["a", "c"])
        # Both components yield length 2
        assert len(result) == 2


# ===========================================================================
# _connector_path and _message_flow_path
# ===========================================================================


class TestConnectorPath:
    def test_side_by_side(self):
        src = (0, -100, 110, -160)  # left, top, right, bottom (EA convention)
        tgt = (150, -100, 260, -160)
        result = _connector_path(src, tgt)
        assert result is not None
        parts = result.strip(";").split(";")
        # Should have 1 waypoint: midpoint x between boxes
        assert len(parts) == 1
        mx, my = parts[0].split(":")
        expected_mx = int((110 + 150) / 2)
        assert int(mx) == expected_mx

    def test_vertical(self):
        src = (0, -100, 110, -160)
        tgt = (50, -300, 160, -360)  # far below
        result = _connector_path(src, tgt)
        # y_disjoint, so waypoint at src cx, tgt cy
        assert result is not None
        parts = result.strip(";").split(";")
        mx, my = parts[0].split(":")
        scx = int((0 + 110) / 2)
        tcy = int((-300 + -360) / 2)
        assert int(mx) == scx
        assert int(my) == tcy

    def test_overlapping_no_path(self):
        # Overlapping boxes -> None (EA auto-routes)
        src = (0, -100, 200, -300)
        tgt = (50, -150, 150, -250)
        assert _connector_path(src, tgt) is None


class TestMessageFlowPath:
    def test_target_below(self):
        src = (0, -100, 110, -160)
        tgt = (50, -300, 160, -360)
        result = _message_flow_path(src, tgt)
        assert result is not None
        parts = result.strip(";").split(";")
        assert len(parts) == 2  # 2 waypoints (elbow)
        mx1, my1 = parts[0].split(":")
        mx2, my2 = parts[1].split(":")
        scx = int((0 + 110) / 2)
        tcx = int((50 + 160) / 2)
        my_elbow = int((-160 + -300) / 2)
        assert int(mx1) == scx
        assert int(my1) == my_elbow
        assert int(mx2) == tcx

    def test_target_above(self):
        src = (0, -300, 110, -360)
        tgt = (50, -100, 160, -160)
        result = _message_flow_path(src, tgt)
        assert result is not None
        parts = result.strip(";").split(";")
        assert len(parts) == 2
        my_elbow = int((-360 + -100) / 2)
        assert int(parts[0].split(":")[1]) == my_elbow

    def test_vertically_aligned_uses_two_waypoints(self):
        scx = 55
        tcx = 55
        src = (0, -100, 110, -160)
        tgt = (0, -300, 110, -360)
        result = _message_flow_path(src, tgt)
        assert result is not None
        # Still two waypoints (vertical alignment doesn't collapse to one)
        parts = result.strip(";").split(";")
        assert len(parts) == 2

    def test_not_vertically_separated_falls_back(self):
        src = (0, -100, 110, -160)
        tgt = (150, -100, 260, -160)
        result = _message_flow_path(src, tgt)
        # Falls back to _connector_path
        assert result is not None
        parts = result.strip(";").split(";")
        assert len(parts) == 1


# ===========================================================================
# BPMN config mapping completeness
# ===========================================================================


class TestBpmnConfigMaps:
    def test_label_to_stereo_has_all_types(self):
        for t in ("Activity", "StartEvent", "EndEvent", "IntermediateEvent", "Gateway",
                   "ExclusiveGateway", "ParallelGateway", "Lane", "Pool",
                   "DataObject", "TextAnnotation"):
            assert t in LABEL_TO_STEREO, f"Missing {t} in LABEL_TO_STEREO"

    def test_object_type_map_has_all_stereos(self):
        for stereo in LABEL_TO_STEREO.values():
            assert stereo in OBJECT_TYPE_MAP or stereo == "CollaborationModel"

    def test_bpmn_tagged_values_has_core_stereos(self):
        """Only some BPMN types define tagged values; missing types are fine."""
        for stereo in ("Activity", "StartEvent", "EndEvent", "IntermediateEvent",
                        "Gateway", "ExclusiveGateway", "ParallelGateway",
                        "Lane", "DataObject"):
            assert stereo in BPMN_TAGGED_VALUES, f"Missing {stereo} in BPMN_TAGGED_VALUES"

    def test_connector_maps_have_same_keys(self):
        cats = ("SequenceFlow", "MessageFlow", "DataOutputAssociation", "DataInputAssociation")
        for c in cats:
            assert c in CONNECTOR_TYPES
            assert c in CONNECTOR_STEREOTYPE_EX

    def test_bpmn_element_sizes_has_core_types(self):
        """CollaborationModel, Lane, and Pool are structural (not diagram-objects) and
        don't need a size entry. All visual BPMN types should have one."""
        for size_type in ("Activity", "Task", "StartEvent", "EndEvent",
                           "IntermediateEvent", "Gateway", "Decision",
                           "ExclusiveGateway", "ParallelGateway",
                           "DataObject", "DataStore", "TextAnnotation", "Artifact"):
            assert size_type in BPMN_ELEMENT_SIZES, f"Missing {size_type} in BPMN_ELEMENT_SIZES"


# ===========================================================================
# MD parsing
# ===========================================================================


SAMPLE_MD_FLAT = textwrap.dedent("""\
## Collaboration—collab1
- Name: My Collaboration
- Description: A test

### Lane—lane1
- Name: Customer Lane

### StartEvent—start1
- Name: Start Process
- Lane: lane1

### Activity—act1
- Name: Do Something
- Lane: lane1

### Sequence Flows

- start1 → act1

### Data Output Associations

- start1 → act1
""")

SAMPLE_MD_HIER = textwrap.dedent("""\
## Collaboration—collab1
- Name: Newsletter

### Lane—lane1
- Name: Newsletter Lane

#### StartEvent—start1
- Name: Start

#### Activity—act1
- Name: Process

### Sequence Flows
- start1 ➡ act1
""")


class TestParseMdFlat:
    @pytest.fixture
    def md_file(self, tmp_path):
        p = tmp_path / "test_flat.md"
        p.write_text(SAMPLE_MD_FLAT, encoding="utf-8")
        return str(p)

    def test_parse_elements(self, md_file):
        elements, connectors = _parse_md_flat(md_file, ("SequenceFlow", "DataOutputAssociation"))
        assert "collab1" in elements
        assert elements["collab1"]["label"] == "Collaboration"
        assert elements["collab1"]["fields"].get("Name") == "My Collaboration"
        assert "lane1" in elements
        assert elements["lane1"]["label"] == "Lane"
        assert elements["lane1"]["fields"].get("Name") == "Customer Lane"
        assert "start1" in elements
        assert elements["start1"]["label"] == "StartEvent"
        assert "act1" in elements
        assert elements["act1"]["label"] == "Activity"

    def test_parse_connectors(self, md_file):
        elements, connectors = _parse_md_flat(md_file, ("SequenceFlow", "DataOutputAssociation"))
        assert "SequenceFlow" in connectors
        assert len(connectors["SequenceFlow"]) == 1
        assert connectors["SequenceFlow"][0]["source"] == "start1"
        assert connectors["SequenceFlow"][0]["target"] == "act1"
        assert "DataOutputAssociation" in connectors
        assert len(connectors["DataOutputAssociation"]) == 1

    def test_parse_empty(self, tmp_path):
        p = tmp_path / "empty.md"
        p.write_text("", encoding="utf-8")
        elements, connectors = _parse_md_flat(str(p), ("SequenceFlow",))
        assert elements == {}
        assert connectors == {"SequenceFlow": []}

    def test_parse_connector_with_condition(self, tmp_path):
        md = textwrap.dedent("""\
        ### Sequence Flows
        - src → tgt [yes]
        """)
        p = tmp_path / "cond.md"
        p.write_text(md, encoding="utf-8")
        elements, connectors = _parse_md_flat(str(p), ("SequenceFlow",))
        assert connectors["SequenceFlow"][0]["condition"] == "yes"

    def test_parse_connector_with_unicode_arrow(self, tmp_path):
        md = textwrap.dedent("""\
        ### Sequence Flows
        - src ➡ tgt
        """)
        p = tmp_path / "uni.md"
        p.write_text(md, encoding="utf-8")
        elements, connectors = _parse_md_flat(str(p), ("SequenceFlow",))
        assert connectors["SequenceFlow"][0]["source"] == "src"
        assert connectors["SequenceFlow"][0]["target"] == "tgt"

    def test_fields_preserved(self, md_file):
        elements, connectors = _parse_md_flat(md_file, ("SequenceFlow",))
        assert elements["collab1"]["fields"].get("Name") == "My Collaboration"
        assert elements["collab1"]["fields"].get("Description") == "A test"
        assert elements["start1"]["fields"].get("Lane") == "lane1"


class TestParseMdHierarchical:
    @pytest.fixture
    def md_file(self, tmp_path):
        p = tmp_path / "test_hier.md"
        p.write_text(SAMPLE_MD_HIER, encoding="utf-8")
        return str(p)

    def test_parse_elements(self, md_file):
        elements, connectors = _parse_md_hierarchical(md_file, ("SequenceFlow",))
        assert "collab1" in elements
        assert "lane1" in elements
        assert elements["lane1"]["label"] == "Lane"
        assert "start1" in elements
        assert "act1" in elements

    def test_parse_parent_field(self, md_file):
        elements, connectors = _parse_md_hierarchical(md_file, ("SequenceFlow",))
        # #### elements under a ### Lane get Parent field
        assert elements["start1"]["fields"].get("Parent") == "lane1"

    def test_parse_sequence_flows(self, md_file):
        elements, connectors = _parse_md_hierarchical(md_file, ("SequenceFlow",))
        assert len(connectors["SequenceFlow"]) == 1
        assert connectors["SequenceFlow"][0]["source"] == "start1"
        assert connectors["SequenceFlow"][0]["target"] == "act1"

    def test_empty(self, tmp_path):
        p = tmp_path / "empty.md"
        p.write_text("", encoding="utf-8")
        elements, connectors = _parse_md_hierarchical(str(p), ("SequenceFlow",))
        assert elements == {}
        assert connectors["SequenceFlow"] == []


# ===========================================================================
# compute_bpmn_flow_layout (integrated placement)
# ===========================================================================


class TestComputeBpmnFlowLayout:
    def test_simple_chain(self):
        elements_by_lane = {"lane1": ["a", "b", "c"]}
        lane_bounds = {"lane1": (0, 30, 1000, 530)}
        flows = [
            {"source": "a", "target": "b"},
            {"source": "b", "target": "c"},
        ]
        elem_types = {"a": "Activity", "b": "Activity", "c": "Activity"}
        pos, updated = compute_bpmn_flow_layout(
            elements_by_lane, lane_bounds, flows, elem_types
        )
        assert "a" in pos
        assert "b" in pos
        assert "c" in pos
        # Left-to-right
        assert pos["a"][0] < pos["b"][0] < pos["c"][0]

    def test_data_object_separate_row(self):
        elements_by_lane = {"lane1": ["a", "b", "d1"]}
        lane_bounds = {"lane1": (0, 30, 1000, 530)}
        flows = [{"source": "a", "target": "b"}]
        elem_types = {"a": "Activity", "b": "Activity", "d1": "DataObject"}
        pos, updated = compute_bpmn_flow_layout(
            elements_by_lane, lane_bounds, flows, elem_types
        )
        # DataObject should be below flow elements
        assert pos["d1"][1] > pos["a"][1]
        assert pos["d1"][1] > pos["b"][1]

    def test_fork_places_side_branch_below(self):
        elements_by_lane = {"lane1": ["a", "b", "c"]}
        lane_bounds = {"lane1": (0, 30, 1000, 530)}
        flows = [
            {"source": "a", "target": "b"},
            {"source": "a", "target": "c"},
        ]
        elem_types = {"a": "Gateway", "b": "Activity", "c": "Activity"}
        pos, updated = compute_bpmn_flow_layout(
            elements_by_lane, lane_bounds, flows, elem_types
        )
        # Gateway A is 42px tall, Activity B is 60px — A is centered vertically
        # in the row (top is slightly higher than B). Both share the same row.
        a_top = pos["a"][1]
        a_bot = pos["a"][3]
        b_top = pos["b"][1]
        b_bot = pos["b"][3]
        # B is in the same or overlapping vertical band as A
        assert max(a_top, b_top) < min(a_bot, b_bot), "A and B should overlap vertically (same row)"
        # C (side branch) should be below row 0 (below B's bottom)
        assert pos["c"][1] > b_bot, "C (forked branch) should be below main row"
        # Both should be right of A
        assert pos["b"][0] > pos["a"][0]
        assert pos["c"][0] >= pos["a"][0]


# ===========================================================================
# _bottom_right_positions_for_new
# ===========================================================================


class _FakeDobj:
    def __init__(self, element_id, left, top, right, bottom):
        self.ElementID = element_id
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom


class _FakeDiagramObjects:
    def __init__(self, dobjs):
        self._dobjs = dobjs
        self.Count = len(dobjs)

    def GetAt(self, i):
        return self._dobjs[i]


class _FakeDiag:
    def __init__(self, dobjs):
        self.DiagramObjects = _FakeDiagramObjects(dobjs)


class TestBottomRightPositionsForNew:
    def test_first_new_goes_below_existing_content_in_lane(self):
        # Lane occupies canonical (0,0)-(1000,500).  EA stores top/bottom negated.
        lane_dobj = _FakeDobj(element_id=101, left=0, top=0, right=1000, bottom=-500)
        # One existing Activity in the lane, bottom at canonical y=200.
        existing = _FakeDobj(element_id=201, left=100, top=-100, right=210, bottom=-200)
        diag = _FakeDiag([lane_dobj, existing])

        # lane_id "L1" -> ea_object_id 101; new element "N1" -> ea_object_id 301.
        object_ids = {"L1": 101, "existing": 201, "N1": 301}
        all_by_lane = {"L1": ["existing", "N1"]}
        elem_types = {"existing": "Activity", "N1": "Activity"}
        lane_dobjs = {"L1": lane_dobj}
        new_by_lane = {"L1": ["N1"]}

        pos = _bottom_right_positions_for_new(
            diag, new_by_lane, lane_dobjs, all_by_lane, object_ids, elem_types,
        )

        # N1 should be positioned in the lane, below the existing element (y >= 200 + gap).
        assert "N1" in pos
        l, t, r, b = pos["N1"]
        assert t >= 220, f"N1 top {t} should be below existing bottom (200) + v_gap"
        assert 0 <= l < 1000, f"N1 left {l} should be inside lane"
        assert r <= 1000, f"N1 right {r} should not exceed lane_right"

    def test_starts_below_lane_header_when_lane_empty(self):
        lane_dobj = _FakeDobj(element_id=101, left=0, top=0, right=1000, bottom=-500)
        diag = _FakeDiag([lane_dobj])  # only the lane, no elements

        object_ids = {"L1": 101, "N1": 301}
        all_by_lane = {"L1": ["N1"]}
        elem_types = {"N1": "Activity"}
        lane_dobjs = {"L1": lane_dobj}

        pos = _bottom_right_positions_for_new(
            diag, {"L1": ["N1"]}, lane_dobjs, all_by_lane, object_ids, elem_types,
        )
        _, t, _, _ = pos["N1"]
        # header band = 40, v_gap = 20 -> new element top around 60
        assert 40 < t < 100, f"N1 top {t} should be just below lane header + gap"

    def test_multiple_new_wrap_to_next_row(self):
        # Narrow lane forces wrapping
        lane_dobj = _FakeDobj(element_id=101, left=0, top=0, right=300, bottom=-800)
        diag = _FakeDiag([lane_dobj])
        object_ids = {"L1": 101, "N1": 301, "N2": 302, "N3": 303}
        all_by_lane = {"L1": ["N1", "N2", "N3"]}
        elem_types = {"N1": "Activity", "N2": "Activity", "N3": "Activity"}
        lane_dobjs = {"L1": lane_dobj}

        pos = _bottom_right_positions_for_new(
            diag, {"L1": ["N1", "N2", "N3"]}, lane_dobjs, all_by_lane, object_ids, elem_types,
        )
        # Activities are 110 wide; two fit within lane_right - lane_pad (300 - 20 = 280) → no
        # actually 20 + 110 + 20 + 110 = 260 which fits (< 280).  Third would push x + 110 =
        # 20 + 110 + 20 + 110 + 20 + 110 = 390 > 280 → wraps.
        n3_top = pos["N3"][1]
        n1_top = pos["N1"][1]
        assert n3_top > n1_top, "N3 should wrap to a new row below N1/N2"
