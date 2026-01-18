from fastapi import APIRouter, HTTPException
from typing import List
from beanie import PydanticObjectId
from app.models.course import Course

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("/", response_model=Course, status_code=201)
async def create_course(course: Course):
    await course.insert()
    return course

@router.get("/", response_model=List[Course])
async def get_courses():
    return await Course.find_all(fetch_links=True).to_list()

@router.get("/{id}", response_model=Course)
async def get_course(id: PydanticObjectId):
    course = await Course.get(id, fetch_links=True)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course

@router.put("/{id}", response_model=Course)
async def update_course(id: PydanticObjectId, course_data: Course):
    course = await Course.get(id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    course.title = course_data.title
    course.description = course_data.description
    course.credits = course_data.credits
    course.department = course_data.department
    course.professor = course_data.professor
    
    await course.save()
    return course

@router.delete("/{id}", status_code=204)
async def delete_course(id: PydanticObjectId):
    course = await Course.get(id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    await course.delete()
    return