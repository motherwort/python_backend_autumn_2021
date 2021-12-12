from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Thread


@registry.register_document
class ThreadDocument(Document):
    search_allowed_fields = [
        'title',
        'description',
        'pool',
        'creator'
    ]
    
    pool = fields.TextField(attr="pool.name")
    creator = fields.TextField(attr="creator.username")

    class Index:
        name = 'threads'

    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
    }

    class Django:
        model = Thread
        fields = [
            'title',
            'description',
        ]
