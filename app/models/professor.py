from typing import Optional
from beanie import Document, Link
from app.models.department import Department

class Professor(Document):
    name: str
    email: str
    title: str  # Ex: "PhD", "MSc"
    department: Link[Department]  # Relacionamento 1:N (Um depto tem vários profs)

    class Settings:
        name = "professors"