# app/models/__init__.py

from .department import Department
from .professor import Professor
from .course import Course
from .student import Student

# Opcional: Define o que é exportado se alguém usar "from app.models import *"
__all__ = ["Department", "Professor", "Course", "Student"]