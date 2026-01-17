"""Exportador a formato OpenAPI YAML."""

import yaml
from typing import Dict, Any


def export_yaml(spec: Dict[str, Any]) -> str:
    """
    Exporta el esquema OpenAPI a formato YAML.

    Args:
        spec: Esquema OpenAPI como diccionario

    Returns:
        Esquema OpenAPI en formato YAML
    """
    return yaml.dump(spec, default_flow_style=False, allow_unicode=True, sort_keys=False)
