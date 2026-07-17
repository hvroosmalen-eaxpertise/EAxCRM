"""Shared wireframe config: WireframeFlow dataclass, per-flow instances, and
the Wireframing MDG vocabulary constants -- mirrors bpmn_config.py's split,
but scoped to what wireframes actually need (no lanes, no flow-layout, no
reflow-on-rerun; screens carry explicit per-control bounds instead).

Ground truth for all stereotype/tagged-value names below: the installed
MDGTechnologies/Wireframing.xml technology definition (the online user guide
returned 403 to automated fetches) -- not guessed.
"""
import os
from dataclasses import dataclass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


@dataclass
class WireframeFlow:
    name: str
    package_name: str
    parent_package_name: str = "User Interface"
    default_qea: str = r"M:\EAxCRM\models\EAxCRM.qea"
    default_md: str = ""
    guid_map_file: str = ""
    flow_id: str = ""
    sitemap_diagram_name: str = ""
    diag_guid_key_sitemap: str = "_diagram_sitemap"
    model_id: str = ""
    purpose: str = ""
    header_name: str = ""
    changelog_file: str = ""


CUSTOMER_ACCOUNT_UI = WireframeFlow(
    name="Manage Customer Account UI",
    package_name="Manage Customer Account UI Architecture",
    default_md=r"M:\EAxCRM\models\EAxCRM-CustomerAccountUI.md",
    guid_map_file="customeraccount_ui_guid_map.json",
    flow_id="ManageCustomerAccountUI",
    sitemap_diagram_name="Manage Customer Account UI — Sitemap",
    model_id="cap-ui-eacrm",
    purpose="Wireframe mockups for the Manage Customer Account screens",
    header_name="Manage Customer Account UI",
    changelog_file=os.path.join(SCRIPT_DIR, "customeraccount_ui_changelog.md"),
)


# ---- Wireframing MDG vocabulary ----

# Native EA Diagram_Type for every Wireframing diagram stereotype is
# "Custom" (Diagram_Custom in the MDG XML) -- NOT "Logical"/"Analysis" used
# by ArchiMate/BPMN. The Webpage Wireframe stereotype's own "styleex"
# property is "Whiteboard=1;", which must be combined with the MDGDgm
# toolbox-selector key discovered during the issue #5 investigation.
DIAGRAM_NATIVE_TYPE = "Custom"
DIAGRAM_STEREOTYPE_SHORT = "Webpage Wireframe"
DIAGRAM_STYLEEX_MDGDGM = "Wireframing::Webpage Wireframe"
DIAGRAM_STYLEEX_EXTRA = "Whiteboard=1;"

# The Screen element itself (the webpage container each diagram is built
# from) -- base type Screen, distinct from the GUIElement/Text controls
# placed on it.
SCREEN_STEREOTYPE = "WireframeWebsite"
SCREEN_BASE_TYPE = "Screen"

# MD "- Type:" value -> (EA stereotype short name, base Sparx type).
# Base type is "GUIElement" for most controls, "Text" for text blocks.
# Casing matters for round-tripping: EA normalizes StereotypeEx to the
# canonical name from the <Stereotype name="..."> definition when read back
# (confirmed empirically -- the MDG's own UIToolboxes Tag entries reference
# some of these in a different, non-canonical case, e.g.
# "Wireframing::Wireframebutton(UML::GUIElement)", which still works for
# *creating* the element but reads back as "WireframeButton", breaking the
# reverse stereo-> MD-Type lookup on sync unless the canonical case is used
# here too).
CONTROL_TYPE_TO_STEREO = {
    "Button": ("WireframeButton", "GUIElement"),
    "CheckBox": ("WireframeCheckbox", "GUIElement"),
    "ComboBox": ("WireframeCombobox", "GUIElement"),
    "Image": ("WireframeImage", "GUIElement"),
    "Label": ("WireframeLabel", "GUIElement"),
    "List": ("WireframeList", "GUIElement"),
    "Radio": ("WireframeRadio", "GUIElement"),
    "Table": ("WireframeTable", "GUIElement"),
    "Header": ("WireframeHeader", "GUIElement"),
    "Hyperlink": ("WireframeHyperlink", "GUIElement"),
    "NavigationControl": ("WireframeNavigationControl", "GUIElement"),
    "TextField": ("WireframeTextField", "GUIElement"),
    "TextBlock": ("WireframeTextBlock", "Text"),
    # A nested browser-chrome frame (EA's "Webpage" toolbox item, same
    # stereotype/base-type as a top-level Screen, but placed as a Control
    # nested under one) -- found in the wild 2026-07-06 when the user
    # wrapped a screen's existing controls inside one for visual browser
    # chrome (tabs/address bar are decorative shape rendering, not real
    # child elements). Controls can nest under a Frame the same way a Frame
    # nests under a Screen -- see Control's "- Parent:" field.
    "Frame": ("WireframeWebsite", "Screen"),
}

# Per-control-type tagged value names (from Wireframing.xml's own Tag
# definitions -- already MD-friendly, so no renaming needed, just an
# allow-list per type so an unexpected MD field is caught rather than
# silently set as a stray tagged value). Any "- Field: value" line in a
# Control block matching one of these names is set as that tagged value.
WIREFRAME_TAGGED_VALUES = {
    "Button": {"State"},
    "CheckBox": {"Enabled", "State"},
    "ComboBox": {"DropDownState", "Items"},
    "Radio": {"Enabled", "State"},
    "Label": {"Align Text", "Multiline"},
}

# Navigation links are plain UML Association connectors between Screen
# elements (no dedicated navigation-connector stereotype exists in the
# Wireframing MDG -- this is a project convention, not an EA built-in).
NAVIGATION_CONNECTOR_TYPE = "Association"
