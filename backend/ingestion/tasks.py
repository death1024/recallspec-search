from celery import Celery
from ..adapters.cpsc import CPSCAdapter
from ..adapters.nhtsa import NHTSAAdapter
from ..db.elasticsearch import es_client
import os

celery_app = Celery('recallspec', broker=os.getenv('REDIS_URL', 'redis://localhost:6379'))

@celery_app.task
async def sync_cpsc_recalls():
    """Sync CPSC recalls to Elasticsearch"""
    adapter = CPSCAdapter()
    recalls = await adapter.fetch_recalls(days_back=1825)

    for recall in recalls:
        doc = recall.dict()
        es_client.index(
            index="recalls",
            id=str(recall.id),
            body=doc
        )

    return f"Synced {len(recalls)} CPSC recalls"

@celery_app.task
def sync_nhtsa_recalls():
    """Sync NHTSA recalls - placeholder for bulk import"""
    return "NHTSA sync not yet implemented"
