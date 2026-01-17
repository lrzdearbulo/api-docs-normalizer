"""Exportador a formato OpenAPI JSON."""

import json
from typing import Dict, Any


def export_json(spec: Dict[str, Any]) -> str:
    """
    Exporta el esquema OpenAPI a formato JSON.

    Args:
        spec: Esquema OpenAPI como diccionario

    Returns:
        Esquema OpenAPI en formato JSON
    """
    return json.dumps(spec, indent=2, ensure_ascii=False)
