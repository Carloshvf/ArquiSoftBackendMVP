"""
Integração com a Overpass API (OpenStreetMap) — serviço externo público e gratuito,
usado para descobrir restaurantes próximos a uma coordenada.
Documentação: https://wiki.openstreetmap.org/wiki/Overpass_API
"""
import requests

OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def buscar_restaurantes_proximos(lat: float, lng: float, raio_metros: int = 1000):
    query = f"""
    [out:json][timeout:25];
    (
      node["amenity"="restaurant"](around:{raio_metros},{lat},{lng});
      way["amenity"="restaurant"](around:{raio_metros},{lat},{lng});
    );
    out center tags;
    """

    headers = {
        "User-Agent": "restaurantes-favoritos-mvp/1.0 (projeto academico)",
        "Accept": "application/json",
    }

    response = requests.post(OVERPASS_URL, data={"data": query}, headers=headers, timeout=30)
    response.raise_for_status()
    dados = response.json()

    resultados = []
    for elemento in dados.get("elements", []):
        tags = elemento.get("tags", {})

        if elemento["type"] == "node":
            lat_el, lng_el = elemento.get("lat"), elemento.get("lon")
        else:
            centro = elemento.get("center", {})
            lat_el, lng_el = centro.get("lat"), centro.get("lon")

        if lat_el is None or lng_el is None:
            continue

        resultados.append(
            {
                "osm_id": f'{elemento["type"]}/{elemento["id"]}',
                "nome": tags.get("name", "Restaurante sem nome"),
                "endereco": tags.get("addr:street"),
                "latitude": lat_el,
                "longitude": lng_el,
                "categoria": tags.get("cuisine"),
            }
        )

    return resultados