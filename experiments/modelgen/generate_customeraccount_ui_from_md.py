"""Generate the "Manage Customer Account UI" wireframes in EAxCRM.qea from Markdown.

Usage:
    python generate_customeraccount_ui_from_md.py

Thin wrapper over the shared wireframe_engine/wireframe_config (see issue #4,
docs/superpowers/specs/2026-07-06-wireframe-diagrams-design.md).
"""
import argparse
import wireframe_engine
from wireframe_config import CUSTOMER_ACCOUNT_UI


def main():
    parser = argparse.ArgumentParser(description="Generate Manage Customer Account UI wireframes in EA")
    parser.add_argument("--qea", default=CUSTOMER_ACCOUNT_UI.default_qea)
    parser.add_argument("--md", default=CUSTOMER_ACCOUNT_UI.default_md)
    args = parser.parse_args()
    wireframe_engine.generate(CUSTOMER_ACCOUNT_UI, qea_path=args.qea, md_path=args.md)


if __name__ == "__main__":
    main()
