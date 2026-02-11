"""
PYTHONPATH=. uv run scripts/generate_openapi.py
"""

import json

from app.main import app

with open("openapi.json", "w") as f:
    json.dump(app.openapi(), f, indent=2)
