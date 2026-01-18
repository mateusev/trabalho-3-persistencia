from fastapi import APIRouter, HTTPException
from typing import List
from beanie import PydanticObjectId
from app.models.student import Student

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=Student, status_code=201)
async def create_student(student: Student):
    await student.insert()
    return student

@router.get("/", response_model=List[Student])
async def get_students():
    # fetch_links=True aqui pode ser pesado se houver muitos cursos, use com cautela
    return await Student.find_all(fetch_links=True).to_list()

@router.get("/{id}", response_model=Student)
async def get_student(id: PydanticObjectId):
    student = await Student.get(id, fetch_links=True)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student

@router.put("/{id}", response_model=Student)
async def update_student(id: PydanticObjectId, student_data: Student):
    student = await Student.get(id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    student.name = student_data.name
    student.email = student_data.email
    student.enrollment_year = student_data.enrollment_year
    student.courses = student_data.courses
    
    await student.save()
    return student

@router.delete("/{id}", status_code=204)
async def delete_student(id: PydanticObjectId):
    student = await Student.get(id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    await student.delete()
    return