"""Shared BPMN config: ProcessConfig dataclass, per-process instances, and the
BPMN vocabulary constants previously copy-pasted across the 3 generate_*_process_from_md.py
and 3 sync_*_process_from_ea.py scripts."""
import os
from dataclasses import dataclass, field

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


@dataclass
class ProcessConfig:
    name: str
    package_name: str
    parent_package_name: str = "Process Architecture"
    default_qea: str = r"M:\EAxCRM\models\EAxCRM.qea"
    default_md: str = ""
    guid_map_file: str = ""
    collab_name: str = ""
    collab_name_like: str = ""
    diagram_name: str = ""
    diagram_type: str = "Analysis"  # native EA Diagram_Type BPMN2.0's "Collaboration"
                                     # stereotype applies to (per MDGTechnologies/BPMN
                                     # 2.0 Technology.xml's Diagram_Analysis Apply block)
                                     # -- was "BusinessProcess", not a real Diagram_Type,
                                     # so the BPMN toolbox never showed by default
                                     # (github issue #5)
    lane_ids_fallback: frozenset = field(default_factory=frozenset)
    hierarchical_format: bool = False  # True: newsletter only (#### + Parent-fallback parse, recursive sync writer)
    generate_connector_categories: tuple = ("SequenceFlow", "MessageFlow",
                                             "DataInputAssociation", "DataOutputAssociation")
    sync_connector_categories: tuple = ("SequenceFlow", "MessageFlow",
                                         "DataInputAssociation", "DataOutputAssociation")
    model_id: str = ""
    purpose: str = ""
    header_name: str = ""
    diag_guid_key: str = ""
    tagged_value_overrides: dict | None = None
    changelog_file: str = ""


CUSTOMER_ACCOUNT = ProcessConfig(
    name="Customer Account",
    package_name="Manage Customer Account Architecture",
    default_md=r"M:\EAxCRM\models\EAxCRM-CustomerAccountProcess.md",
    guid_map_file="customeraccount_guid_map.json",
    collab_name="Manage Customer Account",
    collab_name_like="%Customer Account%",
    diagram_name="Manage Customer Account",
    diag_guid_key="_diagram_customeraccount",
    lane_ids_fallback=frozenset({"EAxpertise"}),
    model_id="cap-eacrm",
    purpose="BPMN 2.0 process model for creating and maintaining Customer Accounts in EAxCRM",
    header_name="Manage Customer Account Process",
    changelog_file=os.path.join(SCRIPT_DIR, "customeraccount_changelog.md"),
)

SALES = ProcessConfig(
    name="Sales",
    package_name="Sales Process Architecture",
    default_md=r"M:\EAxCRM\models\EAxCRM-SalesProcess.md",
    guid_map_file="sales_guid_map.json",
    collab_name="EAxCRM Sales Process Architecture",
    collab_name_like="%Sales%",
    diagram_name="Sales Process Architecture",
    diag_guid_key="_diagram_sales",
    lane_ids_fallback=frozenset({"Customer", "EAxpertise", "Vendor"}),
    model_id="sp-eacrm",
    purpose="BPMN 2.0 sales process model for the EAxCRM system",
    header_name="Sales Process Architecture",
    changelog_file=os.path.join(SCRIPT_DIR, "sales_changelog.md"),
)

NEWSLETTER = ProcessConfig(
    name="Newsletter",
    package_name="Newsletter Process Architecture",
    default_md=r"M:\EAxCRM\models\EAxCRM-NewsletterProcess.md",
    guid_map_file="newsletter_guid_map.json",
    collab_name="EAxCRM Newsletter Process Architecture",
    collab_name_like="%Newsletter%",
    diagram_name="Newsletter Process Architecture",
    diag_guid_key="_diagram_newsletter",
    model_id="nlp-eacrm",
    purpose="BPMN 2.0 newsletter process model for the EAxCRM system",
    header_name="Newsletter Process Architecture",
    changelog_file=os.path.join(SCRIPT_DIR, "newsletter_changelog.md"),
    hierarchical_format=True,
    generate_connector_categories=("SequenceFlow",),
    sync_connector_categories=("SequenceFlow", "MessageFlow"),
)


# ---- Shared BPMN vocabulary (was copy-pasted across generate_*/sync_* scripts) ----

LABEL_TO_STEREO = {
    "BPMN Collaboration": "CollaborationModel",
    "Lane": "Lane",
    "Pool": "Pool",
    "Activity": "Activity",
    "StartEvent": "StartEvent",
    "EndEvent": "EndEvent",
    "IntermediateEvent": "IntermediateEvent",
    "Gateway": "Gateway",
    "ExclusiveGateway": "ExclusiveGateway",
    "ParallelGateway": "ParallelGateway",
    "InclusiveGateway": "InclusiveGateway",
    "ComplexGateway": "ComplexGateway",
    "EventBasedGateway": "EventBasedGateway",
    "DataObject": "DataObject",
    "DataStore": "DataStore",
    "TextAnnotation": "TextAnnotation",
}

OBJECT_TYPE_MAP = {
    "Activity": "Activity",
    "StartEvent": "Event",
    "EndEvent": "Event",
    "IntermediateEvent": "Event",
    "Gateway": "Decision",
    "ExclusiveGateway": "Decision",
    "ParallelGateway": "Gateway",
    "InclusiveGateway": "Gateway",
    "ComplexGateway": "Gateway",
    "EventBasedGateway": "Gateway",
    "Lane": "ActivityPartition",
    "Pool": "ActivityPartition",
    "CollaborationModel": "Activity",
    "DataObject": "Artifact",
    "DataStore": "Artifact",
    "TextAnnotation": "Artifact",
}

BPMN_TAGGED_VALUES = {
    "Activity": {
        "taskType": "Task Type",
        "loopCharacteristics": "Loop",
        "completionQuantity": "Completion Quantity",
        "startQuantity": "Start Quantity",
        "isForCompensation": "Is For Compensation",
        "isACalledActivity": "Is Called Activity",
        "calledElement": "Called Element",
    },
    "SubProcess": {
        "loopCharacteristics": "Loop",
        "completionQuantity": "Completion Quantity",
        "startQuantity": "Start Quantity",
        "isForCompensation": "Is For Compensation",
        "adHoc": "Ad Hoc",
        "adhocOrdering": "Ad Hoc Ordering",
        "adhocCompletionCondition": "Ad Hoc Completion Condition",
    },
    "StartEvent": {
        "eventDefinition": "Event Type",
        "triggerType": "Trigger",
    },
    "EndEvent": {
        "eventDefinition": "Event Type",
        "triggerType": "Result",
    },
    "IntermediateEvent": {
        "eventDefinition": "Event Type",
        "triggerType": "Trigger",
    },
    "Gateway": {
        "gatewayType": "Gateway Type",
    },
    "ExclusiveGateway": {
        "gatewayType": "Gateway Type",
    },
    "ParallelGateway": {
        "gatewayType": "Gateway Type",
    },
    "Lane": {
        "partitionElement": "Partition Element",
    },
    "Pool": {
        "processRef": "Process Ref",
    },
    "CollaborationModel": {
        "isClosed": "Is Closed",
        "mainPool": "Main Pool",
        "correlationKeys": "Correlation Keys",
        "choreographyRef": "Choreography Ref",
    },
    "DataObject": {
        "dataObjectRef": "Data Object Ref",
        "isCollection": "Is Collection",
        "dataInOut": "Data In/Out",
    },
}

CONNECTOR_TYPES = {
    "SequenceFlow": "ControlFlow",
    "MessageFlow": "ControlFlow",
    "DataOutputAssociation": "Dependency",
    "DataInputAssociation": "Dependency",
}

CONNECTOR_STEREOTYPE_EX = {
    "SequenceFlow": "BPMN2.0::SequenceFlow",
    "MessageFlow": "BPMN2.0::MessageFlow",
    "DataOutputAssociation": "BPMN2.0::DataOutputAssociation",
    "DataInputAssociation": "BPMN2.0::DataInputAssociation",
}

CONNECTOR_STEREOTYPES_SHORT = {
    "SequenceFlow": "SequenceFlow",
    "MessageFlow": "MessageFlow",
    "DataOutputAssociation": "DataOutputAssociation",
    "DataInputAssociation": "DataInputAssociation",
}

# Sync-side: EA Object_Type -> MD label (was duplicated across all 3 sync scripts)
BPMN_TYPE_LABEL = {
    "Activity": "Activity",
    "Event": "Event",
    "Decision": "Gateway",
    "Gateway": "Gateway",
    "Object": "DataObject",
    "Artifact": "Artifact",
    "ActivityPartition": "Lane",  # Pool also uses this EA type; sync writers override
                                   # via the element's own Stereotype when it differs
                                   # from its base Object_Type (see set_tagged_values
                                   # callers / write_element in bpmn_engine.sync_to_md)
}

# Type-appropriate dimensions for BPMN elements (width, height in pixels), moved
# from diagram_utils.py -- exclusively used by the BPMN layout functions below.
BPMN_ELEMENT_SIZES = {
    "Activity": (110, 60),
    "Task": (110, 60),
    "StartEvent": (30, 30),
    "EndEvent": (30, 30),
    "IntermediateEvent": (30, 30),
    "Gateway": (42, 42),
    "Decision": (42, 42),
    "ExclusiveGateway": (42, 42),
    "ParallelGateway": (42, 42),
    "InclusiveGateway": (42, 42),
    "ComplexGateway": (42, 42),
    "EventBasedGateway": (42, 42),
    "DataObject": (35, 50),
    "DataStore": (35, 50),
    "TextAnnotation": (80, 50),
    "Artifact": (35, 50),
}
