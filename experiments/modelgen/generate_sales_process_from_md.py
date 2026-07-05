"""Generate the BPMN Sales process in EAxCRM.qea from Markdown.

Usage:
    python generate_sales_process_from_md.py

Thin wrapper over the shared bpmn_engine/bpmn_config (see issue #3 refactor,
docs/superpowers/specs/2026-07-03-bpmn-config-driven-engine-design.md).
"""
import argparse
import bpmn_engine
from bpmn_config import SALES


def main():
    parser = argparse.ArgumentParser(description="Generate Sales process in EA")
    parser.add_argument("--qea", default=SALES.default_qea)
    parser.add_argument("--md", default=SALES.default_md)
    args = parser.parse_args()
    bpmn_engine.generate(SALES, qea_path=args.qea, md_path=args.md)


if __name__ == "__main__":
    main()
