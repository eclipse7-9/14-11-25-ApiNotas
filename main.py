from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Modelo de nota
class Nota(BaseModel):
    titulo: str
    contenido: str

class NotaConID(Nota):
    id: int

# Base de datos temporal en memoria
notas: List[NotaConID] = [
    NotaConID(id=1, titulo="Nota 1", contenido="Contenido de nota 1"),
    NotaConID(id=2, titulo="Nota 2", contenido="Contenido de nota 2"),
]

# GET – Obtener todas las notas
@app.get("/notas", response_model=List[NotaConID])
def obtener_notas():
    return notas

# POST – Crear una nota
@app.post("/notas", response_model=NotaConID, status_code=201)
def crear_nota(nota: Nota):
    nuevo_id = max([n.id for n in notas], default=0) + 1
    nueva_nota = NotaConID(id=nuevo_id, **nota.dict())
    notas.append(nueva_nota)
    return nueva_nota

# PUT – Actualizar una nota
@app.put("/notas/{id}", response_model=NotaConID)
def actualizar_nota(id: int, data: Nota):
    for i, nota in enumerate(notas):
        if nota.id == id:
            notas[i] = NotaConID(id=id, **data.dict())
            return notas[i]
    raise HTTPException(status_code=404, detail="Nota no encontrada")

# DELETE – Eliminar una nota
@app.delete("/notas/{id}")
def eliminar_nota(id: int):
    global notas
    notas = [n for n in notas if n.id != id]
    return {"mensaje": "Nota eliminada"}