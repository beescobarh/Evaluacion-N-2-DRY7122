import requests


GRAPHHOPPER_API_KEY = "cb93d1bf-44b7-400c-8854-605c34f10295" 
GEOCODE_API_URL = "https://graphhopper.com/api/1/geocode"
ROUTE_API_URL = "https://graphhopper.com/api/1/route"


RENDIMIENTO_KM_POR_LITRO = 12.0

def obtener_coordenadas(lugar):
    """Obtiene latitud y longitud a partir del nombre de una ciudad."""
    params = {'q': lugar, 'key': GRAPHHOPPER_API_KEY}
    try:
        response = requests.get(GEOCODE_API_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if data['hits']:
            point = data['hits'][0]['point']
            return f"{point['lat']},{point['lng']}"
    except requests.exceptions.RequestException:
        pass
    return None

def obtener_ruta(coords_origen, coords_destino):
    """Consulta la API de rutas de Graphhopper usando coordenadas."""
    params = {
        'point': [coords_origen, coords_destino],
        'key': GRAPHHOPPER_API_KEY,
        'locale': 'es',
        'instructions': True,
        'calc_points': True,
        'vehicle': 'car'
    }
    try:
        response = requests.get(ROUTE_API_URL, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"🚨 Error de conexión: {e}")
    return None

def mostrar_narrativa_viaje(datos_ruta):
    """Procesa y muestra los datos del viaje según los requerimientos."""
    if not datos_ruta or 'paths' not in datos_ruta or not datos_ruta['paths']:
        print("No se encontró una ruta válida.")
        return

    path = datos_ruta['paths'][0]
    

    distancia_km = path['distance'] / 1000.0
    

    tiempo_ms = path['time']
    segundos_totales = tiempo_ms / 1000.0
    horas = int(segundos_totales // 3600)
    minutos = int((segundos_totales % 3600) // 60)
    segundos = segundos_totales % 60.0
    

    litros_combustible = distancia_km / RENDIMIENTO_KM_POR_LITRO
    
    print("\n" + "="*60)
    print("                     RESUMEN DEL VIAJE")
    print("="*60)

    print(f"📍 Distancia total: {distancia_km:.2f} km")
    print(f"🕒 Duración: {horas:02d} horas, {minutos:02d} minutos y {segundos:.2f} segundos")
    print(f"⛽ Combustible requerido: {litros_combustible:.2f} litros")
    print("="*60)

    print("\n🗺️  NARRATIVA DEL VIAJE:")
    for i, instruccion in enumerate(path['instructions']):
        distancia_instruccion_km = instruccion['distance'] / 1000.0
        print(f"  {i+1}. {instruccion['text']} ({distancia_instruccion_km:.2f} km)")
    
    print("\n✅ ¡Has llegado a tu destino!")
    print("="*60 + "\n")

def main():
    while True:
        print("\n--- Cálculo de Rutas ---")
        print("Ingrese 'q' para salir del programa.")
        
        nombre_origen = input("\nCiudad de Origen: ")
        if nombre_origen.lower() == 'q':
            break
            
        nombre_destino = input("Ciudad de Destino: ")
        if nombre_destino.lower() == 'q':
            break

        print("\nBuscando ruta...")
        coords_origen = obtener_coordenadas(nombre_origen)
        if not coords_origen:
            print(f"❌ No se encontró: '{nombre_origen}'.")
            continue

        coords_destino = obtener_coordenadas(nombre_destino)
        if not coords_destino:
            print(f"❌ No se encontró: '{nombre_destino}'.")
            continue

        datos_ruta = obtener_ruta(coords_origen, coords_destino)
        if datos_ruta:
            mostrar_narrativa_viaje(datos_ruta)

    print("\n👋 Programa finalizado.")

if __name__ == "__main__":
    main()