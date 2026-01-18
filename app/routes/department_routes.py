from fastapi import APIRouter, HTTPException
from typing import List
from beanie import PydanticObjectId
from app.models.department import Department

router = APIRouter(prefix="/departments", tags=["Departments"])

@router.post("/", response_model=Department, status_code=201)
async def create_department(dept: Department):
    await dept.insert()
    return dept

@router.get("/", response_model=List[Department])
async def get_departments():
    return await Department.find_all().to_list()

@router.get("/{id}", response_model=Department)
async def get_department(id: PydanticObjectId):
    dept = await Department.get(id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept

@router.put("/{id}", response_model=Department)
async def update_department(id: PydanticObjectId, dept_data: Department):
    dept = await Department.get(id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    
    dept.name = dept_data.name
    dept.code = dept_data.code
    await dept.save()
    return dept

@router.delete("/{id}", status_code=204)
async def delete_department(id: PydanticObjectId):
    dept = await Department.get(id)
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    await dept.delete()
    return