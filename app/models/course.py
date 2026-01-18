from beanie import Document, Link
from app.models.department import Department
from app.models.professor import Professor

class Course(Document):
    title: str
    description: str | None = None
    credits: int
    department: Link[Department]
    professor: Link[Professor] | None = None # Novo: Prof responsável

    class Settings:
        name = "courses"