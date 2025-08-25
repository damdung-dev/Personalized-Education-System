import random
import faker
import pandas as pd

fake = faker.Faker()

account_types = ["Regular", "Premium", "Trial"]
jobs = ["Student", "Engineer", "Teacher", "Freelancer", "Office Staff", "Unemployed", "Doctor", "IT Specialist", "Marketing", "Sales"]

students = []

for i in range(2000):
    full_name = fake.name()
    dob = fake.date_of_birth(minimum_age=16, maximum_age=40).strftime('%Y-%m-%d')
    username = fake.user_name()
    student_id = f"STU{1000 + i}"
    account_type = random.choice(account_types)
    phone = fake.phone_number()
    email = username + "@gmail.com"
    job = random.choice(jobs)
    listening= round(random.uniform(4.0,9.0), 1)
    reading= round(random.uniform(4.0, 9.0), 1)
    writing= round(random.uniform(4.0, 9.0), 1)
    speaking= round(random.uniform(4.0, 9.0), 1)

    students.append({
        "full_name": full_name,
        "dob": dob,
        "username": username,
        "student_id": student_id,
        "account_type": account_type,
        "phone": phone,
        "email": email,
        "job": job,
        "reading": reading,
        "listening":listening,
        "writing":writing,
        "speaking":speaking,
    })

df = pd.DataFrame(students)
df.to_csv("ielts_students_data.csv", index=False)

students_data=pd.read_csv("ielts_students_data.csv")
print(students_data.head(5))


