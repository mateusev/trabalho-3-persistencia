from beanie import Document
from pydantic import BaseModel

class Department(Document):
    name: str
    code: str  # Ex: "DCC", "MAT"

    class Settings:
        name = "departments"