#!/usr/bin/env python3
"""
Seed script to populate the database with sample todo items
"""

from sqlalchemy.orm import Session
from database import SessionLocal, Todo, engine, Base
from datetime import datetime, timedelta
import random

# Sample todo data
SAMPLE_TODOS = [
    {
        "title": "Complete project documentation",
        "description": "Write comprehensive documentation for the new API endpoints",
        "priority": "high",
        "completed": False
    },
    {
        "title": "Review pull requests",
        "description": "Review and approve pending pull requests from team members",
        "priority": "medium",
        "completed": False
    },
    {
        "title": "Setup CI/CD pipeline",
        "description": "Configure GitHub Actions for automated testing and deployment",
        "priority": "high",
        "completed": True
    },
    {
        "title": "Refactor authentication module",
        "description": "Improve the authentication flow and add OAuth support",
        "priority": "medium",
        "completed": False
    },
    {
        "title": "Write unit tests",
        "description": "Add unit tests for the new features implemented last sprint",
        "priority": "high",
        "completed": False
    },
    {
        "title": "Update dependencies",
        "description": "Update all npm packages to their latest stable versions",
        "priority": "low",
        "completed": True
    },
    {
        "title": "Optimize database queries",
        "description": "Analyze and optimize slow database queries identified in monitoring",
        "priority": "medium",
        "completed": False
    },
    {
        "title": "Schedule team meeting",
        "description": "Schedule weekly sync meeting with the development team",
        "priority": "low",
        "completed": True
    },
    {
        "title": "Implement caching strategy",
        "description": "Add Redis caching for frequently accessed endpoints",
        "priority": "medium",
        "completed": False
    },
    {
        "title": "Fix bug in payment module",
        "description": "Resolve the issue with payment processing for international customers",
        "priority": "high",
        "completed": True
    },
    {
        "title": "Create backup strategy",
        "description": "Implement automated database backup and recovery procedures",
        "priority": "high",
        "completed": False
    },
    {
        "title": "Design new dashboard UI",
        "description": "Create mockups for the new admin dashboard interface",
        "priority": "medium",
        "completed": False
    },
    {
        "title": "Conduct security audit",
        "description": "Perform a comprehensive security audit of the application",
        "priority": "high",
        "completed": False
    },
    {
        "title": "Migrate to TypeScript",
        "description": "Start migrating JavaScript codebase to TypeScript",
        "priority": "low",
        "completed": False
    },
    {
        "title": "Setup monitoring alerts",
        "description": "Configure alerts for critical application metrics",
        "priority": "medium",
        "completed": True
    }
]

def seed_database():
    """Seed the database with sample todo items"""

    # Create a new session
    db = SessionLocal()

    try:
        # Clear existing todos
        db.query(Todo).delete()
        db.commit()
        print("Cleared existing todos...")

        # Add sample todos
        for i, todo_data in enumerate(SAMPLE_TODOS):
            # Create random creation dates within the last 30 days
            days_ago = random.randint(0, 30)
            created_date = datetime.utcnow() - timedelta(days=days_ago)

            # If completed, set a random completion date after creation
            updated_date = created_date
            if todo_data["completed"]:
                days_to_complete = random.randint(1, min(7, days_ago)) if days_ago > 0 else 0
                updated_date = created_date + timedelta(days=days_to_complete)

            todo = Todo(
                title=todo_data["title"],
                description=todo_data["description"],
                priority=todo_data["priority"],
                completed=todo_data["completed"],
                created_at=created_date,
                updated_at=updated_date
            )
            db.add(todo)
            print(f"Added todo {i+1}: {todo_data['title']}")

        # Commit all changes
        db.commit()
        print(f"\nSuccessfully seeded {len(SAMPLE_TODOS)} todos!")

        # Display statistics
        total = db.query(Todo).count()
        completed = db.query(Todo).filter(Todo.completed == True).count()
        high_priority = db.query(Todo).filter(Todo.priority == "high").count()
        medium_priority = db.query(Todo).filter(Todo.priority == "medium").count()
        low_priority = db.query(Todo).filter(Todo.priority == "low").count()

        print("\nDatabase Statistics:")
        print(f"  Total todos: {total}")
        print(f"  Completed: {completed}")
        print(f"  Pending: {total - completed}")
        print(f"  High priority: {high_priority}")
        print(f"  Medium priority: {medium_priority}")
        print(f"  Low priority: {low_priority}")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    # Ensure tables exist
    Base.metadata.create_all(bind=engine)

    # Run the seed function
    seed_database()

    print("\nDatabase seeding complete!")
    print("You can now start the FastAPI server with: uvicorn main:app --reload")