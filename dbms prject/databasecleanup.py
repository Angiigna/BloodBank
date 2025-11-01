from website import create_app
from website import db
from website.models import User, Donor, Request # Import your models for clarity

# 1. Create the Flask app instance
app = create_app()

# 2. Use the application context
with app.app_context():
    print("WARNING: This will permanently delete ALL data in your database!")
    
    # Optional: You can check if data exists before dropping
    user_count = db.session.query(User).count()
    donor_count = db.session.query(Donor).count()
    request_count = db.session.query(Request).count()
    
    print(f"Current data counts: Users ({user_count}), Donors ({donor_count}), Requests ({request_count})")
    
    confirm = input("Are you absolutely sure you want to proceed? Type 'YES' to confirm: ")
    
    if confirm == 'YES':
        try:
            # Step 1: Drop all tables (deletes all data and schema)
            db.drop_all()
            print("Successfully dropped all database tables.")
            
            # Step 2: Recreate all tables (sets up a clean, empty schema)
            db.create_all()
            print("Successfully recreated all database tables. Your database is now empty and ready.")
            
            # Final check
            print(f"New data counts: Users ({db.session.query(User).count()}), Donors ({db.session.query(Donor).count()}), Requests ({db.session.query(Request).count()})")
            
        except Exception as e:
            print(f"An error occurred during cleanup: {e}")
            
    else:
        print("Database reset cancelled. No changes were made.")
