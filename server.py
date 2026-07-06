from mcp.server.fastmcp import FastMCP
import httpx
import sqlite3
import json

# Inicializamos el servidor FastMCP
mcp = FastMCP("MEF_SIAF")

# Ruta de la base de datos local
DB_PATH = "mef_data.db"

@mcp.tool()
async def fetch_mef_dataset(resource_id: str, table_name: str, limit: int = 1000) -> str:
    """
    Descarga un dataset específico del MEF usando su `resource_id` (el cual puedes obtener 
    desde el portal datosabiertos.mef.gob.pe) y lo guarda en la base de datos 
    local (SQLite) bajo el nombre de tabla `table_name`. 
    Si la tabla ya existe, la sobrescribe.
    """
    url = f"https://api.datosabiertos.mef.gob.pe/DatosAbiertos/v1/datastore_search?resource_id={resource_id}&limit={limit}"
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, timeout=30.0)
            if response.status_code != 200:
                return f"Error HTTP {response.status_code}: {response.text}"
                
            data = response.json()
            if not data.get("success"):
                return "Error: la API del MEF indicó success=false"
                
            records = data["result"]["records"]
            if not records:
                return "No se encontraron registros."
                
            # Extraemos los nombres de las columnas del primer registro
            columns = list(records[0].keys())
            
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            
            # Crear tabla dinámicamente en SQLite (Typeless)
            cols_def = ", ".join([f'"{col}" TEXT' for col in columns])
            cursor.execute(f'DROP TABLE IF EXISTS "{table_name}"')
            cursor.execute(f'CREATE TABLE "{table_name}" ({cols_def})')
            
            # Insertar datos
            placeholders = ", ".join(["?" for _ in columns])
            insert_query = f'INSERT INTO "{table_name}" VALUES ({placeholders})'
            
            for row in records:
                values = [str(row.get(col, "")) for col in columns]
                cursor.execute(insert_query, values)
                
            conn.commit()
            conn.close()
            
            return f"Éxito: Se crearon {len(records)} registros reales en la tabla '{table_name}' desde la API del MEF."
            
    except Exception as e:
        return f"Excepción al descargar dataset: {str(e)}"

@mcp.tool()
def sql_mef_db(query: str) -> str:
    """
    Ejecuta una consulta SQL nativa en la base de datos local del MEF (mef_data.db).
    Puedes hacer JOINs entre tablas que hayas descargado previamente.
    Retorna los resultados en formato JSON.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(query)
        
        if query.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            conn.close()
            return json.dumps({"columnas": columns, "filas": results}, indent=2)
        else:
            conn.commit()
            conn.close()
            return json.dumps({"status": "success", "message": "Consulta ejecutada correctamente."})
            
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

if __name__ == "__main__":
    mcp.run(transport='stdio')
