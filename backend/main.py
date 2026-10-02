import json

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Buku(BaseModel):
    id: int
    judul: str
    penulis: str
    kategori: str
    stok: int = Field(ge=0)

class BukuBaru(BaseModel):
    judul: str
    penulis: str
    kategori: str
    stok: int = Field(ge=0)

with open("data/books.json", "r", encoding="utf-8") as file:
    daftar_buku = json.load(file)

@app.get("/")
def home():
    return {
        "message": "API Dashboard Perpustakaan berjalan"
    }

@app.get("/buku", response_model=list[Buku])
def get_buku():
    return daftar_buku

@app.post("/buku", response_model=Buku)
def tambah_buku(buku: BukuBaru):
    id_baru = max([item["id"] for item in daftar_buku], default=0) + 1

    data_baru = {
        "id": id_baru,
        "judul": buku.judul,
        "penulis": buku.penulis,
        "kategori": buku.kategori,
        "stok": buku.stok
    }

    daftar_buku.append(data_baru)

    return data_baru

@app.delete("/buku/{id}")
def hapus_buku(id: int):
    for buku in daftar_buku:
        if buku["id"] == id:
            daftar_buku.remove(buku)

            return {
                "message": "Buku berhasil dihapus"
            }

    raise HTTPException(
        status_code=404,
        detail="Buku tidak ditemukan"
    )