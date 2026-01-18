from fastapi import APIRouter, HTTPException
from typing import List
from beanie import PydanticObjectId
from app.models.professor import Professor

router = APIRouter(prefix="/professors", tags=["Professors"])

@router.post("/", response_model=Professor, status_code=201)
async def create_professor(prof: Professor):
    # Dica: O JSON de entrada deve conter o link do departamento corretamente
    await prof.insert()
    return prof

@router.get("/", response_model=List[Professor])
async def get_professors():
    # fetch_links=True traz os dados do Departamento junto, não só o ID
    return await Professor.find_all(fetch_links=True).to_list()

@router.get("/{id}", response_model=Professor)
async def get_professor(id: PydanticObjectId):
    prof = await Professor.get(id, fetch_links=True)
    if not prof:
        raise HTTPException(status_code=404, detail="Professor not found")
    return prof

@router.put("/{id}", response_model=Professor)
async def update_professor(id: PydanticObjectId, prof_data: Professor):
    prof = await Professor.get(id)
    if not prof:
        raise HTTPException(status_code=404, detail="Professor not found")
    
    prof.name = prof_data.name
    prof.email = prof_data.email
    prof.title = prof_data.title
    prof.department = prof_data.department
    
    await prof.save()
    return prof

@router.delete("/{id}", status_code=204)
async def delete_professor(id: PydanticObjectId):
    prof = await Professor.get(id)
    if not prof:
        raise HTTPException(status_code=404, detail="Professor not found")
    await prof.delete()
    return