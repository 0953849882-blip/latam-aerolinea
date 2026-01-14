from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI(title="LATAM - API Consulta de Vuelos", version="1.0.0")

class Vuelo(BaseModel):
    id: int
    aerolinea: str
    origen: str
    destino: str
    fecha: str        # YYYY-MM-DD
    hora: str         # HH:MM
    asientos_disponibles: int
    precio_usd: float

# Dataset de ejemplo (puedes ampliarlo)
VUELOS = [
    Vuelo(id=1, aerolinea="LATAM", origen="UIO", destino="GYE", fecha="2026-01-16", hora="08:30", asientos_disponibles=12, precio_usd=89.99),
    Vuelo(id=2, aerolinea="LATAM", origen="UIO", destino="CUE", fecha="2026-01-16", hora="10:15", asientos_disponibles=5, precio_usd=74.50),
    Vuelo(id=3, aerolinea="LATAM", origen="GYE", destino="UIO", fecha="2026-01-17", hora="14:40", asientos_disponibles=20, precio_usd=92.00),
    Vuelo(id=4, aerolinea="LATAM", origen="UIO", destino="LIM", fecha="2026-01-18", hora="06:10", asientos_disponibles=8, precio_usd=199.99),
]

@app.get("/health")
def health():
    return {"status": "ok", "time": datetime.utcnow().isoformat() + "Z"}

@app.get("/vuelos", response_model=List[Vuelo])
def buscar_vuelos(
    origen: Optional[str] = Query(default=None, description="Código IATA ej: UIO"),
    destino: Optional[str] = Query(default=None, description="Código IATA ej: GYE"),
    fecha: Optional[str] = Query(default=None, description="YYYY-MM-DD"),
    min_asientos: int = Query(default=1, ge=1),
):
    resultados = VUELOS

    if origen:
        resultados = [v for v in resultados if v.origen.upper() == origen.upper()]
    if destino:
        resultados = [v for v in resultados if v.destino.upper() == destino.upper()]
    if fecha:
        resultados = [v for v in resultados if v.fecha == fecha]

    resultados = [v for v in resultados if v.asientos_disponibles >= min_asientos]
    return resultados

@app.get("/vuelos/{vuelo_id}", response_model=Vuelo)
def detalle_vuelo(vuelo_id: int):
    for v in VUELOS:
        if v.id == vuelo_id:
            return v
    return {"detail": "Vuelo no encontrado"}
