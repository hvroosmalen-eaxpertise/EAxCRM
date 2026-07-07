"""Generate the BPMN Newsletter process in EAxCRM.qea from Markdown.

Usage:
    python generate_newsletter_process_from_md.py

Thin wrapper over the shared bpmn_engine/bpmn_config (see issue #3 refactor,
docs/superpowers/specs/2026-07-03-bpmn-config-driven-engine-design.md).
Exercises bpmn_config.NEWSLETTER's hierarchical_format (#### + Parent-fallback
parsing), reflow_on_rerun, and single-category (SequenceFlow only) connector
handling -- the most complex of the 3 BPMN configs.
"""
import argparse
import bpmn_engine
from bpmn_config import NEWSLETTER


def main():
    parser = argparse.ArgumentParser(description="Generate newsletter process model in EA")
    parser.add_argument("--qea", default=NEWSLETTER.default_qea)
    parser.add_argument("--md", default=NEWSLETTER.default_md)
    parser.add_argument("--state-dir", default=None,
                         help="Directory for the changelog and GUID-map files (default: script dir). "
                              "Override in tests so runs against a sandboxed --qea don't touch the real ones.")
    args = parser.parse_args()
    bpmn_engine.generate(NEWSLETTER, qea_path=args.qea, md_path=args.md, state_dir=args.state_dir)


if __name__ == "__main__":
    main()
