"""Interfaz de línea de comandos para api-docs-normalizer."""

import sys
import argparse
from pathlib import Path
from typing import Optional, Dict, Any

from .parser import Parser
from .normalizer import Normalizer
from .cache import Cache
from .exporters.openapi_yaml import export_yaml
from .exporters.openapi_json import export_json


class Processor:
    """Orquesta el procesamiento de archivos de documentación."""

    def __init__(self):
        self.parser = Parser()
        self.normalizer = Normalizer()
        self.cache = Cache()

    def process_file(
        self, input_path: str, output_path: Optional[str], output_format: str
    ) -> None:
        """
        Procesa un archivo de entrada y genera la salida normalizada.

        Args:
            input_path: Ruta al archivo de entrada
            output_path: Ruta al archivo de salida (opcional)
            output_format: Formato de salida (yaml o json)
        """
        input_file = Path(input_path)
        self._validate_input_file(input_file)

        content = self._read_input_file(input_file)
        spec = self._get_or_process_spec(content, input_file.stem)

        output_file = self._determine_output_file(input_file, output_path, output_format)
        self._write_output_file(output_file, spec, output_format)

        print(f"Output written to: {output_file}")

    def _validate_input_file(self, input_file: Path) -> None:
        """
        Valida que el archivo de entrada exista.

        Args:
            input_file: Path al archivo de entrada

        Raises:
            FileNotFoundError: Si el archivo no existe
        """
        if not input_file.exists():
            raise FileNotFoundError(f"El archivo {input_file} no existe")

    def _read_input_file(self, input_file: Path) -> str:
        """
        Lee el contenido del archivo de entrada.

        Args:
            input_file: Path al archivo de entrada

        Returns:
            Contenido del archivo
        """
        with open(input_file, "r", encoding="utf-8") as f:
            return f.read()

    def _get_or_process_spec(self, content: str, title: str) -> Dict[str, Any]:
        """
        Obtiene el esquema desde cache o lo procesa.

        Args:
            content: Contenido del archivo
            title: Título para la API

        Returns:
            Esquema OpenAPI como diccionario
        """
        content_hash = self.cache.get_hash(content)

        if self.cache.exists(content_hash):
            print("[cache] using cached result", file=sys.stderr)
            cached_result = self.cache.get(content_hash)
            if cached_result:
                return cached_result
            # Si el cache está corrupto, procesar de nuevo

        spec = self._process_content(content, title)
        self.cache.set(content_hash, spec)
        return spec

    def _process_content(self, content: str, title: str) -> Dict[str, Any]:
        """
        Procesa el contenido y genera el esquema OpenAPI.

        Args:
            content: Contenido del archivo
            title: Título para la API

        Returns:
            Esquema OpenAPI como diccionario
        """
        endpoints = self.parser.parse(content)

        if not endpoints:
            print("Warning: No se detectaron endpoints en el archivo", file=sys.stderr)

        return self.normalizer.normalize(endpoints, title=title)

    def _determine_output_file(
        self, input_file: Path, output_path: Optional[str], output_format: str
    ) -> Path:
        """
        Determina la ruta del archivo de salida.

        Args:
            input_file: Path al archivo de entrada
            output_path: Ruta de salida especificada (opcional)
            output_format: Formato de salida

        Returns:
            Path al archivo de salida
        """
        if output_path:
            return Path(output_path)

        extension = ".yaml" if output_format == "yaml" else ".json"
        return input_file.with_suffix(extension)

    def _write_output_file(
        self, output_file: Path, spec: Dict[str, Any], output_format: str
    ) -> None:
        """
        Escribe el esquema OpenAPI al archivo de salida.

        Args:
            output_file: Path al archivo de salida
            spec: Esquema OpenAPI
            output_format: Formato de salida
        """
        if output_format == "yaml":
            output_content = export_yaml(spec)
        else:
            output_content = export_json(spec)

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(output_content)


def main():
    """Punto de entrada principal del CLI."""
    parser = argparse.ArgumentParser(
        description="Normaliza documentación de APIs a OpenAPI 3.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "input",
        type=str,
        help="Archivo de entrada con documentación de la API (Markdown o texto plano)",
    )

    parser.add_argument(
        "-o",
        "--out",
        type=str,
        default=None,
        help="Archivo de salida (por defecto: input con extensión .yaml o .json)",
    )

    parser.add_argument(
        "-f",
        "--format",
        choices=["yaml", "json"],
        default="yaml",
        help="Formato de salida (default: yaml)",
    )

    args = parser.parse_args()

    try:
        processor = Processor()
        processor.process_file(args.input, args.out, args.format)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
