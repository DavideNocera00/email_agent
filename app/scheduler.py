from apscheduler.schedulers.background import BackgroundScheduler
from app.database import SessionLocal
from app.models import User
from app.agent.digest_builder import run_agent_for_user
from app import crud

scheduler = BackgroundScheduler()

def run_agent_for_all_users():
    db = SessionLocal()
    try:
        users = db.query(User).filter(User.google_refresh_token.isnot(None)).all()
        for user in users:
            try:
                result = run_agent_for_user(user.google_refresh_token)
                crud.save_digest(db, user.id, result["digest_text"], result["items"])
                print(f"Digest generato per {user.email}")
            except Exception as e:
                print(f"Errore nella generazione del digest per {user.email}: {e}")
    finally:
        db.close()

#run the method run_agent_for_all_users every 24 hours
def start_scheduler():
    scheduler.add_job(run_agent_for_all_users, "interval", hours=24)
    scheduler.start()