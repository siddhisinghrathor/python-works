def calculate_grade(score):
    if score >= 90:
        return "A"
    elif score >= 80:
        return "B"
    elif score >= 70:
        return "C"
    elif score >= 60:
        return "D"
    else:
        return "F"

names = {"sid", "nil", "raunak", "gautham"}
score = {20 , 100, 70, 80}

def generate_student_report(name, score):
    grade = calculate_grade(score)
    return f"{name} has Scored {score} and received the Grade: {grade}"

for name, score in zip(names, score):
    report = generate_student_report(name, score)
    print(report)