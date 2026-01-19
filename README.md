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
        +department
    }
    class Course {
        +ObjectId id
        +String title
        +Int credits
        +department
        +professor
    }
    class Student {
        +ObjectId id
        +String name
        +Int enrollment_year
        +List courses
    }

    Department "1" --> "*" Professor
    Department "1" --> "*" Course 
    Professor "1" --> "*" Course 
    Student "*" <--> "*" Course 

    ```
