import asyncio
from server import mef_search_datasets, fetch_mef_dataset, sql_mef_db

async def main():
    print("--- 1. Buscando dataset del Canon ---")
    res_search = await mef_search_datasets("canon minero")
    print("Resultados de búsqueda:")
    print(res_search)
    
    # Extraemos el primer ID del json devuelto para probar la descarga
    import json
    data = json.loads(res_search)
    
    if data:
        primer_resource_id = data[0]["resource_id"]
        print(f"\n--- 2. Descargando el dataset {primer_resource_id} (limit 100) ---")
        res_fetch = await fetch_mef_dataset(primer_resource_id, "canon_minero", limit=100)
        print(res_fetch)
        
        print("\n--- 3. Ejecutando consulta SQL real sobre los datos del Canon ---")
        # Dependiendo del año, las columnas varían, seleccionamos todo con limit 5 para ver la estructura
        query = "SELECT * FROM canon_minero LIMIT 5"
        print(f"Consulta: {query}")
        res_sql = sql_mef_db(query)
        print(res_sql)

if __name__ == "__main__":
    asyncio.run(main())
