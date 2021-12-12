from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Post


@registry.register_document
class PostDocument(Document):
    search_allowed_fields = [
        'content',
        'thread',
        'user'
    ]

    thread = fields.TextField(attr="thread.title")
    user = fields.TextField(attr="user.username")

    class Index:
        name = 'posts'

    settings = {
        'number_of_shards': 1,
        'number_of_replicas': 0
    }

    class Django:
        model = Post
        fields = [
            'content',
        ]
