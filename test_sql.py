import asyncio
from server import fetch_mef_datos_abiertos, sql_mef_db

async def main():
    print("--- 1. Poblado de datos desde la API simulada ---")
    # Llamamos a la herramienta que trae los datos y los inserta en la base de datos local
    res1 = await fetch_mef_datos_abiertos()
    print(res1)
    
    print("\n--- 2. Ejecutando consulta SQL ---")
    # Consulta: Mostrar departamentos ordenados por su gasto ejecutado (devengado) de mayor a menor
    query = "SELECT departamento, pim, devengado FROM ejecucion_presupuestal ORDER BY devengado DESC"
    print(f"Consulta: {query}")
    
    # Llamamos a la herramienta SQL
    res2 = sql_mef_db(query)
    print("\nResultados en JSON (Lo que verá el LLM):")
    print(res2)

if __name__ == "__main__":
    asyncio.run(main())
