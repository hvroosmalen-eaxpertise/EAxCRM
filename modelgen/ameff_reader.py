"""Parse AMEFF 3.1 ArchiMate Exchange Format files."""
import xml.etree.ElementTree as ET

AMEFF_NS = "http://www.opengroup.org/xsd/archimate/3.1/"
XSI_NS = "http://www.w3.org/2001/XMLSchema-instance"

ARCHIMATE_TYPE_TO_SPARX = {
    # Business Layer
    "BusinessActor": "ArchiMate3::ArchiMate_BusinessActor",
    "BusinessRole": "ArchiMate3::ArchiMate_BusinessRole",
    "BusinessFunction": "ArchiMate3::ArchiMate_BusinessFunction",
    "BusinessProcess": "ArchiMate3::ArchiMate_BusinessProcess",
    "BusinessObject": "ArchiMate3::ArchiMate_BusinessObject",
    "BusinessService": "ArchiMate3::ArchiMate_BusinessService",
    "BusinessInteraction": "ArchiMate3::ArchiMate_BusinessInteraction",
    # Application Layer
    "ApplicationComponent": "ArchiMate3::ArchiMate_ApplicationComponent",
    "ApplicationCollaboration": "ArchiMate3::ArchiMate_ApplicationCollaboration",
    "ApplicationInterface": "ArchiMate3::ArchiMate_ApplicationInterface",
    "ApplicationService": "ArchiMate3::ArchiMate_ApplicationService",
    "ApplicationFunction": "ArchiMate3::ArchiMate_ApplicationFunction",
    "ApplicationProcess": "ArchiMate3::ArchiMate_ApplicationProcess",
    "DataObject": "ArchiMate3::ArchiMate_DataObject",
    # Technology Layer
    "Node": "ArchiMate3::ArchiMate_Node",
    "Device": "ArchiMate3::ArchiMate_Device",
    "SystemSoftware": "ArchiMate3::ArchiMate_SystemSoftware",
    "TechnologyService": "ArchiMate3::ArchiMate_TechnologyService",
    "Artifact": "ArchiMate3::ArchiMate_Artifact",
    "CommunicationNetwork": "ArchiMate3::ArchiMate_CommunicationNetwork",
    "Path": "ArchiMate3::ArchiMate_Path",
    # Motivational / Composite
    "Grouping": "ArchiMate3::ArchiMate_Grouping",
    "Location": "ArchiMate3::ArchiMate_Location",
}

ARCHIMATE_RELATION_TO_SPARX = {
    "CompositionRelationship": "ArchiMate3::ArchiMate_Composition",
    "AggregationRelationship": "ArchiMate3::ArchiMate_Aggregation",
    "AssignmentRelationship": "ArchiMate3::ArchiMate_Assignment",
    "RealizationRelationship": "ArchiMate3::ArchiMate_Realization",
    "AssociationRelationship": "ArchiMate3::ArchiMate_Association",
    "TriggeringRelationship": "ArchiMate3::ArchiMate_Triggering",
    "FlowRelationship": "ArchiMate3::ArchiMate_Flow",
    "ServingRelationship": "ArchiMate3::ArchiMate_Serving",
    "AccessRelationship": "ArchiMate3::ArchiMate_Access",
    "InfluenceRelationship": "ArchiMate3::ArchiMate_Influence",
    "SpecializationRelationship": "ArchiMate3::ArchiMate_Specialization",
}

# Layers for package structure
LAYER_PACKAGES = {
    "Business": "Business Layer",
    "Application": "Application Layer",
    "Technology": "Technology Layer",
    "Composite": "Composite Elements",
    "Motivational": "Motivational Elements",
}

ELEMENT_LAYER = {
    # Business
    "BusinessActor": "Business", "BusinessRole": "Business",
    "BusinessFunction": "Business", "BusinessProcess": "Business",
    "BusinessObject": "Business", "BusinessService": "Business",
    "BusinessInteraction": "Business",
    # Application
    "ApplicationComponent": "Application", "ApplicationCollaboration": "Application",
    "ApplicationInterface": "Application", "ApplicationService": "Application",
    "ApplicationFunction": "Application", "ApplicationProcess": "Application",
    "DataObject": "Application",
    # Technology
    "Node": "Technology", "Device": "Technology",
    "SystemSoftware": "Technology", "TechnologyService": "Technology",
    "Artifact": "Technology", "CommunicationNetwork": "Technology",
    # Composite / Motivational
    "Grouping": "Composite", "Location": "Composite",
}


def parse_ameff(path):
    """Parse an AMEFF 3.1 file. Returns dict with elements and relationships."""
    tree = ET.parse(path)
    root = tree.getroot()

    # Register namespace for xsi:type lookups
    ns = {"": AMEFF_NS, "xsi": XSI_NS}

    elements = []
    relations = []

    elements_node = root.find("elements")
    if elements_node is not None:
        for elem_node in elements_node:
            if elem_node.tag != "element":
                continue
            ameff_type = elem_node.get(f"{{{XSI_NS}}}type")
            identifier = elem_node.get("identifier")
            name_el = elem_node.find(f"{{{AMEFF_NS}}}name")
            doc_el = elem_node.find(f"{{{AMEFF_NS}}}documentation")
            name = name_el.text if name_el is not None else ""
            doc = doc_el.text if doc_el is not None else ""
            layer = ELEMENT_LAYER.get(ameff_type, "Business")
            elements.append({
                "id": identifier,
                "ameff_type": ameff_type,
                "name": name,
                "doc": doc,
                "layer": layer,
                "sparx_stereotype": ARCHIMATE_TYPE_TO_SPARX.get(ameff_type, ""),
            })

    rels_node = root.find("relationships")
    if rels_node is not None:
        for rel_node in rels_node:
            if rel_node.tag != "relationship":
                continue
            ameff_type = rel_node.get(f"{{{XSI_NS}}}type")
            identifier = rel_node.get("identifier")
            name_el = rel_node.find(f"{{{AMEFF_NS}}}name")
            source = rel_node.find(f"{{{AMEFF_NS}}}source")
            target = rel_node.find(f"{{{AMEFF_NS}}}target")
            name = name_el.text if name_el is not None else ""
            src_ref = source.get("ref") if source is not None else None
            tgt_ref = target.get("ref") if target is not None else None
            relations.append({
                "id": identifier,
                "ameff_type": ameff_type,
                "name": name,
                "source": src_ref,
                "target": tgt_ref,
                "sparx_stereotype": ARCHIMATE_RELATION_TO_SPARX.get(ameff_type, ""),
            })

    return elements, relations


def build_element_map(elements):
    """Build dict mapping element ID -> element info."""
    return {e["id"]: e for e in elements}
