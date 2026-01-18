from fastapi import APIRouter
from typing import List, Dict, Any
from beanie.operators import RegEx, GTE, In
from beanie import PydanticObjectId

# Importando Modelos
from app.models.student import Student
from app.models.course import Course
from app.models.professor import Professor
from app.models.department import Department

router = APIRouter(prefix="/queries", tags=["Consultas Complexas"])

# a) Consultas por ID (Ex: Detalhes de um Professor e seu Departamento)
@router.get("/professor-details/{id}", response_model=Professor)
async def get_professor_details(id: PydanticObjectId):
    return await Professor.get(id, fetch_links=True)

# b) Listagens filtradas por relacionamentos: Cursos de um Professor
@router.get("/professor/{professor_id}/courses", response_model=List[Course])
async def get_courses_by_professor(professor_id: PydanticObjectId):
    # Busca cursos onde o ID do professor associado é igual ao fornecido
    return await Course.find(Course.professor.id == professor_id).to_list()

# c) Busca por texto parcial (Nome do Estudante)
@router.get("/students/search", response_model=List[Student])
async def search_students(name_part: str):
    # O operador 'i' torna a busca case-insensitive
    return await Student.find(RegEx(Student.name, name_part, "i")).to_list()

# d) Filtros por data/ano (Alunos matriculados a partir de um ano)
@router.get("/students/since/{year}", response_model=List[Student])
async def students_since(year: int):
    return await Student.find(GTE(Student.enrollment_year, year)).to_list()

# e) Agregações: Contagem de cursos por Professor
@router.get("/stats/courses-per-professor")
async def count_courses_per_professor():
    pipeline = [
        {"$group": {"_id": "$professor.$id", "total": {"$sum": 1}}}
    ]
    return await Course.aggregate(pipeline).to_list()

# f) Classificações: Professores ordenados por nome
@router.get("/professors/sorted", response_model=List[Professor])
async def list_professors_sorted():
    # O '+' indica ascendente (A-Z)
    return await Professor.find_all().sort(+Professor.name).to_list()

# g) Consulta complexa: Emails de alunos que têm aula com um Professor
@router.get("/professor/{professor_id}/students-emails")
async def get_students_of_professor(professor_id: PydanticObjectId):
    # 1. Pega os cursos do professor
    courses = await Course.find(Course.professor.id == professor_id).to_list()
    if not courses:
        return []
    
    # Extrai IDs dos cursos
    course_ids = [c.id for c in courses]
    
    # 2. Busca alunos cujos cursos estejam na lista 'course_ids'
    students = await Student.find(In(Student.courses.id, course_ids)).to_list()
    
    return [s.email for s in students]

# h) Quantidade total de filmes (adaptado para Cursos)
@router.get("/stats/total-courses")
async def total_courses():
    count = await Course.count()
    return {"total_courses": count}

# i) Quantidade de atores por filme (adaptado: Alunos por Curso)
@router.get("/stats/students-per-course")
async def students_per_course():
    # Requer agregação no lado do Student, pois é ele quem segura o array de cursos
    pipeline = [
        {"$unwind": "$courses"}, # Expande o array de cursos
        {"$group": {"_id": "$courses.id", "total_students": {"$sum": 1}}}
    ]
    return await Student.aggregate(pipeline).to_list()

# j) Filtro numérico (adaptado: Cursos com créditos acima de X)
@router.get("/courses/high-credits/{min_credits}", response_model=List[Course])
async def high_credit_courses(min_credits: int):
    return await Course.find(GTE(Course.credits, min_credits)).to_list()