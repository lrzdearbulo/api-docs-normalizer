"""Parser para extraer endpoints HTTP de documentación no estructurada."""

import re
from typing import List, Optional


class Endpoint:
    """Representa un endpoint HTTP detectado."""

    def __init__(
        self,
        method: str,
        path: str,
        description: Optional[str] = None,
        parameters: Optional[List[str]] = None,
    ):
        self.method = method.upper()
        self.path = path
        self.description = description or ""
        self.parameters = parameters or []

    def __repr__(self):
        return f"Endpoint({self.method} {self.path})"


class Parser:
    """Parsea documentación Markdown/texto para extraer endpoints HTTP."""

    # Patrones de detección
    HTTP_METHODS = r"(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS)"
    ENDPOINT_PATTERN = re.compile(
        rf"^{HTTP_METHODS}\s+(/[^\s]+)",
        re.IGNORECASE | re.MULTILINE,
    )
    PARAM_PATTERN = re.compile(r"\{(\w+)\}")

    # Configuración de extracción de descripción
    MAX_DESCRIPTION_LINES = 3

    def parse(self, content: str) -> List[Endpoint]:
        """
        Parsea el contenido y extrae endpoints HTTP.

        Args:
            content: Contenido del archivo de documentación

        Returns:
            Lista de endpoints detectados
        """
        lines = content.split("\n")
        endpoints = []

        for line_index, line in enumerate(lines):
            endpoint = self._parse_line_for_endpoint(line, lines, line_index)
            if endpoint:
                endpoints.append(endpoint)

        return endpoints

    def _parse_line_for_endpoint(
        self, line: str, all_lines: List[str], line_index: int
    ) -> Optional[Endpoint]:
        """
        Intenta parsear una línea para detectar un endpoint.

        Args:
            line: Línea actual a analizar
            all_lines: Todas las líneas del documento
            line_index: Índice de la línea actual

        Returns:
            Endpoint detectado o None
        """
        match = self.ENDPOINT_PATTERN.match(line.strip())
        if not match:
            return None

        method = match.group(1)
        path = match.group(2)
        parameters = self._extract_path_parameters(path)
        description = self._extract_description(all_lines, line_index)

        return Endpoint(
            method=method,
            path=path,
            description=description,
            parameters=parameters,
        )

    def _extract_path_parameters(self, path: str) -> List[str]:
        """
        Extrae los nombres de parámetros de una ruta.

        Args:
            path: Ruta del endpoint (ej: /users/{id})

        Returns:
            Lista de nombres de parámetros
        """
        return self.PARAM_PATTERN.findall(path)

    def _extract_description(self, lines: List[str], start_index: int) -> str:
        """
        Extrae la descripción del endpoint desde las líneas siguientes.

        Args:
            lines: Todas las líneas del documento
            start_index: Índice de la línea donde está el endpoint

        Returns:
            Descripción extraída o cadena vacía
        """
        description_parts = []
        current_index = start_index + 1
        end_index = min(
            current_index + self.MAX_DESCRIPTION_LINES,
            len(lines)
        )

        for line_index in range(current_index, end_index):
            line = lines[line_index].strip()

            if self._should_stop_description_extraction(line, description_parts):
                break

            if line:
                description_parts.append(line)

        return " ".join(description_parts).strip()

    def _should_stop_description_extraction(
        self, line: str, description_parts: List[str]
    ) -> bool:
        """
        Determina si se debe detener la extracción de descripción.

        Args:
            line: Línea actual
            description_parts: Partes de descripción ya extraídas

        Returns:
            True si se debe detener, False en caso contrario
        """
        # Detener si encontramos otro endpoint
        if self.ENDPOINT_PATTERN.match(line):
            return True

        # Detener si encontramos un encabezado Markdown
        if line.startswith("#"):
            return True

        # Detener si encontramos una línea vacía y ya tenemos contenido
        if not line and description_parts:
            return True

        return False
