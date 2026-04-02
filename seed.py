"""
Seed the database with demo users and student records.
Runs on every startup but skips insertion if records already exist.
"""
from database import SessionLocal
from auth_utils import hash_password
import models


DEMO_USERS = [
    {
        "name":     "Admin User",
        "email":    "admin@demo.com",
        "password": "Admin@123",
        "role":     models.UserRole.admin,
    },
    {
        "name":     "John Viewer",
        "email":    "user@demo.com",
        "password": "User@123",
        "role":     models.UserRole.user,
    },
]

DEMO_STUDENTS = [
    {
        "name":        "Alice Johnson",
        "email":       "alice.johnson@university.edu",
        "roll_number": "CS2021001",
        "department":  "Computer Science",
        "semester":    6,
        "gpa":         9.2,
        "phone":       "+1-555-0101",
        "address":     "123 Elm Street, Springfield",
    },
    {
        "name":        "Bob Martinez",
        "email":       "bob.martinez@university.edu",
        "roll_number": "EC2021042",
        "department":  "Electronics Engineering",
        "semester":    4,
        "gpa":         8.5,
        "phone":       "+1-555-0102",
        "address":     "456 Oak Avenue, Shelbyville",
    },
    {
        "name":        "Priya Sharma",
        "email":       "priya.sharma@university.edu",
        "roll_number": "ME2022015",
        "department":  "Mechanical Engineering",
        "semester":    3,
        "gpa":         8.9,
        "phone":       "+91-9876543210",
        "address":     "789 MG Road, Bengaluru",
    },
    {
        "name":        "David Kim",
        "email":       "david.kim@university.edu",
        "roll_number": "IT2020088",
        "department":  "Information Technology",
        "semester":    8,
        "gpa":         7.8,
        "phone":       "+82-10-1234-5678",
        "address":     "321 Gangnam-gu, Seoul",
    },
    {
        "name":        "Sara Al-Rashid",
        "email":       "sara.alrashid@university.edu",
        "roll_number": "AI2023005",
        "department":  "Artificial Intelligence",
        "semester":    2,
        "gpa":         9.6,
        "phone":       "+971-50-123-4567",
        "address":     "Dubai Silicon Oasis, Dubai",
    },
]


def seed_data():
    db = SessionLocal()
    try:
        # Seed users
        for u in DEMO_USERS:
            exists = db.query(models.User).filter(models.User.email == u["email"]).first()
            if not exists:
                db.add(models.User(
                    name=u["name"],
                    email=u["email"],
                    password=hash_password(u["password"]),
                    role=u["role"],
                ))

        # Seed students
        for s in DEMO_STUDENTS:
            exists = db.query(models.Student).filter(models.Student.roll_number == s["roll_number"]).first()
            if not exists:
                db.add(models.Student(**s))

        db.commit()
        print("✅  Seed data applied successfully.")
    except Exception as exc:
        db.rollback()
        print(f"⚠️  Seed error (non-fatal): {exc}")
    finally:
        db.close()
