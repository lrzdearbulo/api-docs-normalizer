# API Docs Normalizer

> Transforma documentación de APIs desordenada en esquemas OpenAPI 3.0 listos para producción

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**API Docs Normalizer** es una herramienta CLI que convierte automáticamente documentación de APIs escrita en Markdown o texto plano en esquemas OpenAPI 3.0 estándar, listos para usar con Swagger UI, Postman, Redoc y otras herramientas modernas.

## ✨ Características

- 🚀 **Detección automática** de endpoints HTTP, métodos y parámetros
- 📦 **Cache inteligente** basado en hash SHA256 para evitar reprocesamiento
- 🎯 **OpenAPI 3.0** válido y listo para producción
- 📤 **Exportación flexible** a YAML o JSON
- ⚡ **Rápido y eficiente** - procesa archivos grandes sin problemas
- 🔧 **Zero config** - funciona inmediatamente después de la instalación

## 🎯 Casos de uso

- Migrar documentación legacy a OpenAPI
- Generar documentación interactiva desde notas técnicas
- Integrar en pipelines CI/CD para validación automática
- Convertir documentación de equipos a estándares corporativos
- Preparar APIs para herramientas de testing y mocking

## 🚀 Quick Start

### Instalación

```bash
# Desde el directorio del proyecto
pip install -e .

# O instalar directamente
pip install .
```

### Uso básico

```bash
# Procesa un archivo y genera OpenAPI YAML
api-normalizer docs/api.md

# Especifica el archivo de salida
api-normalizer docs/api.md --out openapi.yaml

# Exporta a JSON
api-normalizer docs/api.md --format json --out openapi.json
```

**¡Eso es todo!** El archivo OpenAPI se genera automáticamente.

## 📖 Ejemplo completo

### Entrada: Documentación desordenada

```markdown
# API de E-commerce

## Usuarios

GET /users
Obtiene la lista completa de usuarios registrados.

POST /users
Crea un nuevo usuario. Requiere email y password.

GET /users/{id}
Obtiene la información de un usuario específico.

DELETE /users/{id}
Elimina un usuario del sistema.

## Productos

GET /products
Lista todos los productos disponibles.

POST /products/{productId}
Crea un nuevo producto en el catálogo.
```

### Salida: OpenAPI 3.0 limpio

```yaml
openapi: 3.0.0
info:
  title: API de E-commerce
  version: 1.0.0
  description: API normalizada desde documentación no estructurada
servers:
  - url: https://api.example.com
    description: Servidor de producción
tags:
  - name: products
  - name: users
paths:
  /users:
    get:
      summary: Obtiene la lista completa de usuarios registrados.
      operationId: get_users
      tags:
        - users
      responses:
        '200':
          description: Respuesta exitosa
          content:
            application/json:
              schema:
                type: object
    post:
      summary: Crea un nuevo usuario. Requiere email y password.
      operationId: post_users
      tags:
        - users
      responses:
        '200':
          description: Respuesta exitosa
          content:
            application/json:
              schema:
                type: object
  /users/{id}:
    get:
      summary: Obtiene la información de un usuario específico.
      operationId: get_users_by_id
      tags:
        - users
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
          description: Identificador del id
      responses:
        '200':
          description: Respuesta exitosa
          content:
            application/json:
              schema:
                type: object
    delete:
      summary: Elimina un usuario del sistema.
      operationId: delete_users_by_id
      tags:
        - users
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
          description: Identificador del id
      responses:
        '200':
          description: Respuesta exitosa
          content:
            application/json:
              schema:
                type: object
  /products:
    get:
      summary: Lista todos los productos disponibles.
      operationId: get_products
      tags:
        - products
      responses:
        '200':
          description: Respuesta exitosa
          content:
            application/json:
              schema:
                type: object
  /products/{productId}:
    post:
      summary: Crea un nuevo producto en el catálogo.
      operationId: post_products_by_productId
      tags:
        - products
      parameters:
        - name: productId
          in: path
          required: true
          schema:
            type: string
          description: Identificador del productId
      responses:
        '200':
          description: Respuesta exitosa
          content:
            application/json:
              schema:
                type: object
```

## 🔍 Detección automática

La herramienta detecta automáticamente:

- **Métodos HTTP**: `GET`, `POST`, `PUT`, `DELETE`, `PATCH`, `HEAD`, `OPTIONS`
- **Rutas con parámetros**: `/users/{id}`, `/products/{productId}/reviews/{reviewId}`
- **Descripciones**: Texto que aparece después de cada endpoint
- **Agrupación por tags**: Organiza endpoints por el primer segmento de la ruta

### Formatos soportados

```markdown
GET /users
Obtiene todos los usuarios

POST /users/{id}
Crea un nuevo usuario

PUT /api/v1/products/{productId}
Actualiza un producto existente

DELETE /orders/{orderId}/items/{itemId}
Elimina un item de un pedido
```

## 💾 Sistema de cache

El sistema de cache inteligente mejora significativamente el rendimiento:

### ¿Cómo funciona?

- **Hash SHA256**: Cada archivo se identifica por su contenido
- **Cache local**: Los resultados se guardan en `~/.api-docs-normalizer/cache/`
- **Detección automática**: Si el contenido no cambió, se usa el resultado cacheado
- **Transparente**: Funciona automáticamente, sin configuración

### Ventajas

✅ **Rapidez**: No reprocesa archivos idénticos  
✅ **Eficiencia**: Ideal para CI/CD y scripts automatizados  
✅ **Transparente**: Verás `[cache] using cached result` cuando se use cache  

### Ejemplo

```bash
# Primera ejecución - procesa el archivo
$ api-normalizer docs/api.md
Output written to: docs/api.yaml

# Segunda ejecución - usa cache
$ api-normalizer docs/api.md
[cache] using cached result
Output written to: docs/api.yaml
```

## 🛠️ Opciones de CLI

```bash
api-normalizer <input> [opciones]

Argumentos:
  input                  Archivo de entrada (Markdown o texto plano)

Opciones:
  -o, --out PATH         Archivo de salida (default: input con extensión .yaml)
  -f, --format FORMAT    Formato de salida: yaml o json (default: yaml)
  -h, --help             Muestra la ayuda
```

### Ejemplos de uso

```bash
# Básico - genera .yaml con el mismo nombre
api-normalizer api.md

# Especificar salida
api-normalizer api.md --out openapi.yaml

# Exportar a JSON
api-normalizer api.md --format json

# Combinar opciones
api-normalizer api.md --format json --out spec.json
```

## 🐳 Uso con Docker

### Construir la imagen

```bash
docker build -t api-normalizer .
```

### Usar el contenedor

```bash
# Procesar un archivo montando el directorio actual
docker run --rm -v $(pwd):/work -w /work api-normalizer examples/messy_api.md

# Especificar archivo de salida
docker run --rm -v $(pwd):/work -w /work api-normalizer examples/messy_api.md --out openapi.yaml

# Exportar a JSON
docker run --rm -v $(pwd):/work -w /work api-normalizer examples/messy_api.md --format json
```

**Nota sobre el cache**: El cache se guarda en `~/.api-docs-normalizer/cache/` dentro del contenedor. Para persistir el cache entre ejecuciones, monta un volumen:

```bash
docker run --rm \
  -v $(pwd):/work \
  -v api-normalizer-cache:/root/.api-docs-normalizer \
  -w /work \
  api-normalizer examples/messy_api.md
```

## 🔗 Integración con otras herramientas

Una vez generado el esquema OpenAPI, puedes usarlo con:

- **Swagger UI**: Visualización interactiva
- **Postman**: Importar y generar colecciones
- **Redoc**: Documentación elegante y responsive
- **OpenAPI Generator**: Generar clientes SDK
- **Prism**: Mocking de APIs
- **Spectral**: Validación de esquemas

### Ejemplo: Swagger UI

```bash
# Generar OpenAPI
api-normalizer docs/api.md --out openapi.yaml

# Usar con Swagger UI (requiere Docker)
docker run -p 8080:8080 -e SWAGGER_JSON=/openapi.yaml -v $(pwd):/usr/share/nginx/html swaggerapi/swagger-ui
```

## 📋 Requisitos

- **Python**: >= 3.10
- **Dependencias**: PyYAML >= 6.0

## 🏗️ Arquitectura

El proyecto está diseñado con una arquitectura modular y clara:

```
api-docs-normalizer/
├── api_normalizer/
│   ├── parser.py          # Extrae endpoints de documentación
│   ├── normalizer.py      # Convierte a esquema OpenAPI 3.0
│   ├── cache.py           # Sistema de cache con SHA256
│   ├── cli.py             # Interfaz de línea de comandos
│   └── exporters/
│       ├── openapi_yaml.py # Exportador YAML
│       └── openapi_json.py # Exportador JSON
├── examples/              # Ejemplos de uso
│   ├── messy_api.md       # Documentación de ejemplo
│   └── output.yaml        # Salida generada
├── README.md
├── pyproject.toml
└── LICENSE
```

### Flujo de procesamiento

1. **Parser**: Detecta endpoints y extrae información
2. **Normalizer**: Convierte a esquema OpenAPI 3.0
3. **Cache**: Verifica si existe resultado cacheado
4. **Exporter**: Genera YAML o JSON según formato solicitado

## 🤝 Contribuir

Las contribuciones son bienvenidas. Para cambios importantes:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## License

MIT © 2026 Luis Ruiz de Arbulo

## 🙋 FAQ

**P: ¿Funciona con documentación en otros idiomas?**  
R: Sí, la herramienta detecta endpoints independientemente del idioma de las descripciones.

**P: ¿Puedo personalizar el esquema OpenAPI generado?**  
R: Actualmente genera esquemas estándar. Para personalización avanzada, edita el YAML generado.

**P: ¿Cómo limpio el cache?**  
R: Elimina el directorio `~/.api-docs-normalizer/cache/` o archivos individuales por hash.

**P: ¿Soporta otros formatos de entrada?**  
R: Actualmente soporta Markdown y texto plano. Otros formatos pueden agregarse en el futuro.

---

**Hecho con ❤️ para desarrolladores que aman las APIs bien documentadas**
