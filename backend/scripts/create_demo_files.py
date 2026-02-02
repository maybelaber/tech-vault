#!/usr/bin/env python3
"""Create demo static files (e.g. figma_components.md) for /demo serving."""

import os

# demo/ is relative to backend/ (parent of scripts/)
DEMO_DIR = os.path.join(os.path.dirname(__file__), "..", "demo")
FIGMA_MD = os.path.join(DEMO_DIR, "figma_components.md")

CONTENT = """# Figma Components

This is a sample file served from FastAPI.

You can use this demo to verify that static file serving works when you click "Open Resource" in TechVault.
"""


def main() -> None:
    os.makedirs(DEMO_DIR, exist_ok=True)
    with open(FIGMA_MD, "w", encoding="utf-8") as f:
        f.write(CONTENT)
    print(f"Created {FIGMA_MD}")


if __name__ == "__main__":
    main()
