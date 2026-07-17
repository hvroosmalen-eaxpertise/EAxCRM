"""Read Newsletter BPMN process model from EAxCRM.qea and write as Markdown.

Usage:
    python sync_newsletter_process_from_ea.py

Thin wrapper over the shared bpmn_engine/bpmn_config (see issue #3 refactor,
docs/superpowers/specs/2026-07-03-bpmn-config-driven-engine-design.md).
Exercises bpmn_config.NEWSLETTER's hierarchical_format (recursive MD writer)
-- the most complex of the 3 BPMN configs.
"""
import argparse
import bpmn_engine
from bpmn_config import NEWSLETTER


def main():
    parser = argparse.ArgumentParser(description=f"Sync {NEWSLETTER.package_name} from EA to Markdown")
    parser.add_argument("--qea", default=NEWSLETTER.default_qea)
    parser.add_argument("--md", default=NEWSLETTER.default_md)
    args = parser.parse_args()
    bpmn_engine.sync_to_md(NEWSLETTER, qea_path=args.qea, md_path=args.md)


if __name__ == "__main__":
    main()
