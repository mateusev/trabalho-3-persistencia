from typing import List
from beanie import Document, Link
from pydantic import EmailStr
from app.models.course import Course

class Student(Document):
    name: str
    email: EmailStr
    enrollment_year: int
    courses: list[Link[Course]] = []  # Relacionamento N:N

    class Settings:
        name = "students"