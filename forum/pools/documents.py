from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Pool


@registry.register_document
class PoolDocument(Document):
    search_allowed_fields = [
        'name',
        'description',
        'creator'
    ]

    creator = fields.TextField(attr="creator.username")

    class Index:
        name = 'pools'

    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
    }

    class Django:
        model = Pool
        fields = [
            'name',
            'description',
        ]
