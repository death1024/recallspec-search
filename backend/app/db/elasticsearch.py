from elasticsearch import Elasticsearch
import os

ES_URL = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
es_client = Elasticsearch([ES_URL])

def create_recalls_index():
    index_name = "recalls"
    if es_client.indices.exists(index=index_name):
        return

    mapping = {
        "mappings": {
            "properties": {
                "authority": {"type": "keyword"},
                "authority_record_id": {"type": "keyword"},
                "category": {"type": "keyword"},
                "product_name": {
                    "type": "text",
                    "fields": {
                        "keyword": {"type": "keyword"},
                        "ngram": {"type": "text", "analyzer": "ngram_analyzer"}
                    }
                },
                "brand": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
                "model": {"type": "keyword"},
                "identifiers": {"type": "object"},
                "hazard": {"type": "text"},
                "recall_date": {"type": "date"},
                "full_text": {"type": "text"}
            }
        },
        "settings": {
            "analysis": {
                "analyzer": {
                    "ngram_analyzer": {
                        "type": "custom",
                        "tokenizer": "ngram_tokenizer"
                    }
                },
                "tokenizer": {
                    "ngram_tokenizer": {
                        "type": "ngram",
                        "min_gram": 3,
                        "max_gram": 4
                    }
                }
            }
        }
    }
    es_client.indices.create(index=index_name, body=mapping)
