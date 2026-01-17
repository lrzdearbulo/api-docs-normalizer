"""Sistema de cache local basado en hash SHA256."""

import hashlib
import json
from pathlib import Path
from typing import Optional, Dict, Any


class Cache:
    """Maneja el cache local de resultados procesados."""

    CACHE_DIR_NAME = ".api-docs-normalizer"
    CACHE_SUBDIR = "cache"
    FILE_EXTENSION = ".json"
    ENCODING = "utf-8"

    def __init__(self):
        self.cache_dir = self._initialize_cache_directory()

    def _initialize_cache_directory(self) -> Path:
        """
        Inicializa y crea el directorio de cache si no existe.

        Returns:
            Path al directorio de cache
        """
        cache_dir = Path.home() / self.CACHE_DIR_NAME / self.CACHE_SUBDIR
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir

    def get_hash(self, content: str) -> str:
        """
        Calcula el hash SHA256 del contenido.

        Args:
            content: Contenido a hashear

        Returns:
            Hash SHA256 en hexadecimal
        """
        return hashlib.sha256(content.encode(self.ENCODING)).hexdigest()

    def get(self, content_hash: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene el resultado cacheado si existe.

        Args:
            content_hash: Hash del contenido

        Returns:
            Resultado cacheado o None si no existe o está corrupto
        """
        cache_file = self._get_cache_file_path(content_hash)

        if not cache_file.exists():
            return None

        try:
            return self._read_cache_file(cache_file)
        except (json.JSONDecodeError, IOError):
            return None

    def set(self, content_hash: str, result: Dict[str, Any]) -> None:
        """
        Guarda el resultado en cache.

        Args:
            content_hash: Hash del contenido
            result: Resultado a cachear
        """
        cache_file = self._get_cache_file_path(content_hash)

        try:
            self._write_cache_file(cache_file, result)
        except IOError:
            # Fallar silenciosamente si no se puede escribir
            pass

    def exists(self, content_hash: str) -> bool:
        """
        Verifica si existe un resultado cacheado.

        Args:
            content_hash: Hash del contenido

        Returns:
            True si existe, False en caso contrario
        """
        cache_file = self._get_cache_file_path(content_hash)
        return cache_file.exists()

    def _get_cache_file_path(self, content_hash: str) -> Path:
        """
        Obtiene la ruta del archivo de cache para un hash dado.

        Args:
            content_hash: Hash del contenido

        Returns:
            Path al archivo de cache
        """
        return self.cache_dir / f"{content_hash}{self.FILE_EXTENSION}"

    def _read_cache_file(self, cache_file: Path) -> Dict[str, Any]:
        """
        Lee el contenido de un archivo de cache.

        Args:
            cache_file: Path al archivo de cache

        Returns:
            Contenido del archivo como diccionario

        Raises:
            json.JSONDecodeError: Si el archivo no es JSON válido
            IOError: Si hay un error de lectura
        """
        with open(cache_file, "r", encoding=self.ENCODING) as f:
            return json.load(f)

    def _write_cache_file(self, cache_file: Path, result: Dict[str, Any]) -> None:
        """
        Escribe el resultado en el archivo de cache.

        Args:
            cache_file: Path al archivo de cache
            result: Resultado a escribir

        Raises:
            IOError: Si hay un error de escritura
        """
        with open(cache_file, "w", encoding=self.ENCODING) as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
