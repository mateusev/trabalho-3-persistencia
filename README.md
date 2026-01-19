```mermaid

classDiagram
    class Department {
        +ObjectId id
        +String name
        +String code
    }
    class Professor {
        +ObjectId id
        +String name
        +String title
        +Link department
    }
    class Course {
        +ObjectId id
        +String title
        +Int credits
        +Link department
        +Link professor
    }
    class Student {
        +ObjectId id
        +String name
        +Int enrollment_year
        +List courses
    }

   
    ```