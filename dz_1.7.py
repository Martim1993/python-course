student_result = {}
students = {
    "Алиса": {"алгебра": 85, "история": 90, "физика": 88},
    "Петр": {"алгебра": 78, "история": 82, "физика": 79},
    "Иван": {"алгебра": 92, "история": 91, "физика": 94},
    "Диана": {"алгебра": 70, "история": 68, "физика": 72},
    "Анна": {"алгебра": 88, "история": 85, "физика": 87}}

students_name = [student for student in students.keys()]
student_grades = [student for student in students.values()]
print(f"{students_name[0]} : {sum(student_grades[0].values())/len(student_grades[0].values())}")

for x in range(len(students)):

    if sum(student_grades[x].values())/len(student_grades[x].values()) > 85:

        student_result[students_name[x]] = "Отличник"

    else:

        student_result[students_name[x]] = "Не отличник"

print(student_result)