# MCP Server - MEF SIAF (Perú)

Este es un servidor **Model Context Protocol (MCP)** diseñado para interactuar con los datos abiertos del **Ministerio de Economía y Finanzas (MEF)** del Perú. 

Permite a los Modelos de Lenguaje (LLMs) descargar dinámicamente conjuntos de datos desde la API oficial de Datos Abiertos del MEF (CKAN) hacia una base de datos local SQLite, y luego ejecutar consultas SQL nativas para realizar análisis económicos.

## Características
- **Extracción de Datos Dinámica:** Descarga cualquier dataset oficial usando su `resource_id`.
- **Motor SQL Integrado:** Los datos se guardan en SQLite para que el LLM pueda hacer joins, agrupaciones y análisis complejos.
- **Rápido y Ligero:** Construido usando `FastMCP` de Anthropic y `uv` para la gestión ultrarrápida del entorno.

## Requisitos Previos
- [uv](https://github.com/astral-sh/uv) instalado.
- Python 3.10 o superior.

## Instalación y Uso

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/tu-usuario/mcp-mef.git
   cd mcp-mef
   ```

2. **Sincronizar el entorno (opcional, uv lo hace automáticamente):**
   ```bash
   uv sync
   ```

3. **Configurar el cliente MCP (Ej. Claude Desktop):**
   Añade lo siguiente a tu archivo `claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "mef-siaf": {
         "command": "uv",
         "args": [
           "run",
           "--directory",
           "Ruta/Absoluta/A/Este/Repositorio",
           "server.py"
         ]
       }
     }
   }
   ```

## Herramientas (Tools) Expuestas al LLM

* `fetch_mef_dataset(resource_id, table_name, limit)`: Descarga un recurso del portal `datosabiertos.mef.gob.pe` y lo inserta como una tabla en la base de datos local.
* `sql_mef_db(query)`: Ejecuta comandos SQL sobre la base de datos local y retorna JSON estructurado para el análisis.

## Advertencia
Los datos obtenidos a través de la API provienen directamente del portal oficial de Datos Abiertos del Gobierno Peruano, pero este proyecto no está afiliado oficialmente al MEF.
