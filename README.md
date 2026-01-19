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
        +List~Link~ courses
    }

    Department "1" --> "*" Professor : lotado_em
    Department "1" --> "*" Course : oferece
    Professor "1" --> "*" Course : ministra
    Student "*" <--> "*" Course : matriculado

    ```