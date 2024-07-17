# app/models/user.py
from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    userPhoto: Optional[str] = None
    namaLengkap: str
    namaPanggilan: str
    tanggalLahir: Optional[str] = None
    gender: Optional[str] = None
    alamatEmail: str
    nomerWhatsapp: str
    pendidikanTerakhir: Optional[str] = None
    alamatProvinsi: Optional[str] = None
    alamatKota: Optional[str] = None
    role: str
