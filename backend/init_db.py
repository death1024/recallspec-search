from app.db.postgres import engine, Base
from app.db.tables import RecallDB, IdentitySpecDB, ResolutionSpecDB
from app.models.watchlist import WatchlistItemDB
from app.models.share import ShareTokenDB, AuditLogDB
from app.db.elasticsearch import create_recalls_index

def init_db():
    """Initialize database tables and Elasticsearch index"""
    Base.metadata.create_all(bind=engine)
    create_recalls_index()
    print("Database initialized successfully")

if __name__ == "__main__":
    init_db()
