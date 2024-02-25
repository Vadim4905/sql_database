import sqlite3

db = sqlite3.connect('database.sql')

db.execute('''CREATE TABLE IF NOT EXISTS students(
           student_id INTEGER PRIMARY KEY AUTOINCREMENT,
           name VARCHAR(50),
           age INTEGER,
           major VARCHAR(50));''')

db.execute('''CREATE TABLE IF NOT EXISTS courses(
           course_id INTEGER PRIMARY KEY AUTOINCREMENT,
           course_name VARCHAR(50),
           instructor  VARCHAR(50));''')

db.execute('''CREATE TABLE IF NOT EXISTS student_course(
           student_id INTEGER REFERENCES students (student_id),
           course_id  INTEGER REFERENCES courses (course_id),
           PRIMARY KEY (student_id,course_id));''')

def add_user(db, name, age, major):
    db.execute(f'''INSERT INTO students(name, age, major)
               VALUES  (?, ?, ?)''', (name, age, major))
    db.commit()
    
def add_course(db, course_name, instructor):
    db.execute(f'''INSERT INTO courses(course_name, instructor)
               VALUES  (?, ?)''', (course_name,instructor))
    db.commit()
    
def get_students(db):
    students = db.execute('''SELECT * FROM students''')
    dict_std = {}
    for student in students:
        dict_std[student[0]] = {'name': student[1], "age": student[2], "major": student[3]}
    db.commit()
    return dict_std

def get_courses(db):
    courses = db.execute('''SELECT * FROM courses''')
    dict_crs= {}
    for course in courses:
        dict_crs[course[0]] = {'course_name': course[1], "instructor": course[2]}
    db.commit()

    return dict_crs

def add_student_to_course(db,student_id,course_id):
    db.execute(f'''INSERT INTO student_course(student_id, course_id)
               VALUES  (?, ?)''', (student_id,course_id))
    db.commit()
    
def get_student_course(db, course_id):
    student_course = db.execute(f'''SELECT * FROM students
                                JOIN student_course ON students.student_id = student_course.student_id
                                WHERE student_course.course_id = ?''', (course_id,))
    
    return student_course

def edit_student(db,student_id,name,age,major):
    db.execute(f'''UPDATE students SET name = ?, age = ?, major = ? WHERE student_id = ?;''',(name,age,major,student_id))
    db.commit()

while True:
    print("\n1. Додати нового студента")
    print("2. Додати новий курс")
    print("3. Показати список студентів")
    print("4. Показати список курсів")
    print("5. Зареєструвати студента на курс")
    print("6. Показати студентів на конкретному курсі")
    print("7. Вийти")

    choice = input("Оберіть опцію (1-7): ")

    if choice == "1":
        # Додавання нового студента
        name = input('input a name ')
        age = input('input a age ')
        major = input('input a major ')
        add_user(db,name,age,major)
        print(f'student {name} added successfully')
        

    elif choice == "2":
        # Додавання нового курсу
        name = input('input a course_name ')
        instructor = input('input a instructor ')
        add_course(db,name,instructor)
        print(f'course {name} added successfully')

    elif choice == "3":
        print(get_students(db))
        # Показати список студентів
     
    elif choice == "4":
        print(get_courses(db))
        # Показати список курсів

    elif choice == "5":
        # Зареєструвати студента на курс
        student_id = int(input('input a student_id '))
        course_id = int(input('input a course_id '))
        add_student_to_course(db,student_id,course_id)
        

    elif choice == "6":
        # Показати студентів на конкретному курсі
        course_id = int(input('input a course_id '))
        students_courses = get_student_course(db,course_id)
        
        for student_course in students_courses:
                print(f"ID: {student_course[0]}, Name: {student_course[1]}, Age: {student_course[2]}, Major: {student_course[3]}")
        
       
    elif choice == "7":
        student_id = int(input('input a student_id '))
        name = input('input a name ')
        age = int(input('input a age '))
        major = input('input a major ')
        edit_student(db,student_id,name,age,major)
        print(f'student {name} edited successfully')
    
    elif choice == "8":
        break

    else:
        print("Некоректний вибір. Будь ласка, введіть число від 1 до 8.")
