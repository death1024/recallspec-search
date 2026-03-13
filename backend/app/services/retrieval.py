from typing import List, Dict
from ..models.specs import ProductIdentitySpec
from ..models.recalls import Recall
from ..db.elasticsearch import es_client
from ..adapters.cpsc import CPSCAdapter
from ..adapters.nhtsa import NHTSAAdapter

class RetrievalEngine:
    """Multi-tier search engine for recalls"""

    def __init__(self):
        self.cpsc = CPSCAdapter()
        self.nhtsa = NHTSAAdapter()

    async def search(self, identity_spec: ProductIdentitySpec) -> List[Dict]:
        """Route and execute search based on identity spec"""

        # Tier 1: Exact match by unique identifiers
        if identity_spec.vin:
            return await self._search_by_vin(identity_spec.vin)

        if identity_spec.upc:
            return await self._search_by_upc(identity_spec.upc)

        # Tier 2: Structured search by brand/model/category
        if identity_spec.brand and identity_spec.category:
            return await self._search_structured(identity_spec)

        # Tier 3: Fuzzy full-text search
        return await self._search_fuzzy(identity_spec)

    async def _search_by_vin(self, vin: str) -> List[Dict]:
        """Exact VIN search via NHTSA"""
        recalls = await self.nhtsa.fetch_recalls_by_vin(vin)
        return [recall.dict() for recall in recalls]

    async def _search_by_upc(self, upc: str) -> List[Dict]:
        """Exact UPC search via Elasticsearch"""
        query = {"term": {"identifiers.upc": upc}}
        result = es_client.search(index="recalls", body={"query": query})
        return [hit["_source"] for hit in result["hits"]["hits"]]

    async def _search_structured(self, identity_spec: ProductIdentitySpec) -> List[Dict]:
        """Structured search by brand/model/category"""
        must_clauses = []

        if identity_spec.brand:
            must_clauses.append({"match": {"brand": identity_spec.brand}})

        if identity_spec.model:
            must_clauses.append({"match": {"model": identity_spec.model}})

        if identity_spec.category:
            must_clauses.append({"term": {"category": identity_spec.category}})

        query = {"bool": {"must": must_clauses}}
        result = es_client.search(index="recalls", body={"query": query, "size": 20})
        return [hit["_source"] for hit in result["hits"]["hits"]]

    async def _search_fuzzy(self, identity_spec: ProductIdentitySpec) -> List[Dict]:
        """Fuzzy full-text search"""
        search_text = f"{identity_spec.brand or ''} {identity_spec.model or ''} {identity_spec.category or ''}"

        query = {
            "multi_match": {
                "query": search_text.strip(),
                "fields": ["product_name^2", "brand", "full_text"],
                "fuzziness": "AUTO"
            }
        }

        result = es_client.search(index="recalls", body={"query": query, "size": 20})
        return [hit["_source"] for hit in result["hits"]["hits"]]
