import os
from application import celery_app
import time
import json
from posts.models import Post


@celery_app.task()
def get_pools_posts():
    posts = Post.objects.filter(is_deleted=False)
    pools_posts = {}
    for post in posts:
        pool = post.thread.pool
        data = {
            'user': post.user.username,
            'thread': post.thread.title,
            'content': post.content
        }
        if str(pool) in pools_posts:
            pools_posts[str(pool)].append(data)
        else:
            pools_posts[str(pool)] = [data]
    with open(f'logs/log-{time.time()}.txt', 'w') as f:
        f.write(json.dumps(pools_posts))
    return json.dumps(pools_posts)

@celery_app.task()
def count_pools_posts():
    posts = Post.objects.filter(is_deleted=False)
    pools_posts = {}
    for post in posts:
        pool = str(post.thread.pool)
        if pool in pools_posts:
            pools_posts[pool] += 1
        else:
            pools_posts[pool] = 1
    with open(f'logs/log-{time.time()}.txt', 'w') as f:
        f.write(json.dumps(pools_posts))
    return json.dumps(pools_posts)