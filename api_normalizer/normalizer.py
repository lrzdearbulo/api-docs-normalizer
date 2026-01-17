"""Normalizador para convertir endpoints en esquema OpenAPI 3.0."""

from typing import List, Dict, Any, Set
from .parser import Endpoint


class Normalizer:
    """Normaliza endpoints a esquema OpenAPI 3.0."""

    # Constantes del esquema OpenAPI
    OPENAPI_VERSION = "3.0.0"
    API_VERSION = "1.0.0"
    DEFAULT_SERVER_URL = "https://api.example.com"
    DEFAULT_SERVER_DESCRIPTION = "Servidor de producción"
    DEFAULT_API_DESCRIPTION = "API normalizada desde documentación no estructurada"

    # Constantes de respuestas
    SUCCESS_STATUS_CODE = "200"
    SUCCESS_DESCRIPTION = "Respuesta exitosa"
    DEFAULT_CONTENT_TYPE = "application/json"

    def normalize(self, endpoints: List[Endpoint], title: str = "API") -> Dict[str, Any]:
        """
        Convierte una lista de endpoints en un esquema OpenAPI 3.0.

        Args:
            endpoints: Lista de endpoints detectados
            title: Título de la API

        Returns:
            Esquema OpenAPI 3.0 como diccionario
        """
        paths = self._build_paths(endpoints)
        tags = self._extract_tags(endpoints)

        return {
            "openapi": self.OPENAPI_VERSION,
            "info": self._build_info_section(title),
            "servers": self._build_servers_section(),
            "tags": self._build_tags_section(tags),
            "paths": paths,
        }

    def _build_paths(self, endpoints: List[Endpoint]) -> Dict[str, Dict[str, Any]]:
        """
        Construye el diccionario de paths agrupando endpoints por ruta.

        Args:
            endpoints: Lista de endpoints

        Returns:
            Diccionario de paths con sus operaciones
        """
        paths = {}

        for endpoint in endpoints:
            if endpoint.path not in paths:
                paths[endpoint.path] = {}

            operation = self._create_operation(endpoint)
            paths[endpoint.path][endpoint.method.lower()] = operation

        return paths

    def _extract_tags(self, endpoints: List[Endpoint]) -> Set[str]:
        """
        Extrae todos los tags únicos de los endpoints.

        Args:
            endpoints: Lista de endpoints

        Returns:
            Conjunto de tags únicos
        """
        return {self._extract_tag_from_path(endpoint.path) for endpoint in endpoints}

    def _build_info_section(self, title: str) -> Dict[str, str]:
        """
        Construye la sección de información de la API.

        Args:
            title: Título de la API

        Returns:
            Diccionario con la información de la API
        """
        return {
            "title": title,
            "version": self.API_VERSION,
            "description": self.DEFAULT_API_DESCRIPTION,
        }

    def _build_servers_section(self) -> List[Dict[str, str]]:
        """
        Construye la sección de servidores.

        Returns:
            Lista de servidores
        """
        return [
            {
                "url": self.DEFAULT_SERVER_URL,
                "description": self.DEFAULT_SERVER_DESCRIPTION,
            }
        ]

    def _build_tags_section(self, tags: Set[str]) -> List[Dict[str, str]]:
        """
        Construye la sección de tags.

        Args:
            tags: Conjunto de tags únicos

        Returns:
            Lista de tags ordenados
        """
        return [{"name": tag} for tag in sorted(tags)]

    def _create_operation(self, endpoint: Endpoint) -> Dict[str, Any]:
        """
        Crea una operación OpenAPI para un endpoint.

        Args:
            endpoint: Endpoint a convertir

        Returns:
            Operación OpenAPI
        """
        tag = self._extract_tag_from_path(endpoint.path)
        summary = endpoint.description or f"{endpoint.method} {endpoint.path}"

        operation = {
            "summary": summary,
            "operationId": self._generate_operation_id(endpoint),
            "tags": [tag],
        }

        if endpoint.description:
            operation["description"] = endpoint.description

        if endpoint.parameters:
            operation["parameters"] = self._create_path_parameters(endpoint.parameters)

        operation["responses"] = self._create_default_responses()

        return operation

    def _create_default_responses(self) -> Dict[str, Dict[str, Any]]:
        """
        Crea las respuestas por defecto para una operación.

        Returns:
            Diccionario de respuestas
        """
        return {
            self.SUCCESS_STATUS_CODE: {
                "description": self.SUCCESS_DESCRIPTION,
                "content": {
                    self.DEFAULT_CONTENT_TYPE: {
                        "schema": {"type": "object"},
                    }
                },
            }
        }

    def _extract_tag_from_path(self, path: str) -> str:
        """
        Extrae el tag del primer segmento de la ruta.

        Args:
            path: Ruta del endpoint (ej: /users/{id})

        Returns:
            Tag extraído (ej: users)
        """
        path_segments = path.split("/")
        if len(path_segments) < 2:
            return "default"

        first_segment = path_segments[1]
        # Remover parámetros de la ruta
        tag = first_segment.split("{")[0]

        return tag or "default"

    def _generate_operation_id(self, endpoint: Endpoint) -> str:
        """
        Genera un operationId único para el endpoint.

        Args:
            endpoint: Endpoint

        Returns:
            operationId generado
        """
        method = endpoint.method.lower()
        path_segments = self._extract_path_segments(endpoint.path)

        if not path_segments:
            return f"{method}_root"

        resource = path_segments[0]

        if endpoint.parameters:
            return f"{method}_{resource}_by_{endpoint.parameters[0]}"

        if len(path_segments) > 1:
            subresource = path_segments[-1]
            return f"{method}_{resource}_{subresource}"

        return f"{method}_{resource}"

    def _extract_path_segments(self, path: str) -> List[str]:
        """
        Extrae los segmentos de la ruta excluyendo parámetros.

        Args:
            path: Ruta del endpoint

        Returns:
            Lista de segmentos de la ruta
        """
        return [
            segment
            for segment in path.split("/")
            if segment and not segment.startswith("{")
        ]

    def _create_path_parameters(self, param_names: List[str]) -> List[Dict[str, Any]]:
        """
        Crea la lista de parámetros de ruta OpenAPI.

        Args:
            param_names: Nombres de los parámetros

        Returns:
            Lista de parámetros OpenAPI
        """
        return [
            {
                "name": param_name,
                "in": "path",
                "required": True,
                "schema": {"type": "string"},
                "description": f"Identificador del {param_name}",
            }
            for param_name in param_names
        ]
