# app/routes/__init__.py

from .department_routes import router as department_router
from .professor_routes import router as professor_router
from .course_routes import router as course_router
from .student_routes import router as student_router
from .query_routes import router as query_router