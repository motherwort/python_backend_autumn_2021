import sys
import aiohttp
import asyncio
from django.core.validators import URLValidator
from requests.sessions import session
import common
import random
from client import get_urls


def read_sys_args():
    argv = sys.argv
    n = int(argv[1])
    k = int(argv[2])
    filename = argv[3]
    return n, k, filename


async def fetch_url(url, k, session, lock):
    if not URLValidator(url):
        return
    async with lock:
        async with session.request('get', url) as resp:
            resp = await session.get(url)
            text = await resp.text()
        data = common.get_k_frequent_words(text, k)
        with open('a_out.txt', 'a') as f:
            f.write(f'{url} : {data}\n')


async def main():
    lock = asyncio.Semaphore(n)
    tasks = []
    async with aiohttp.ClientSession() as session:
        for url in urls:
            task = asyncio.create_task(fetch_url(url, k, session, lock), name=url)
            tasks.append(task)
        await asyncio.gather(*tasks, loop=loop)


if __name__ == '__main__':
    n, k, filename = read_sys_args()
    with open('a_out.txt', 'w') as f:
        f.write('')
    urls = get_urls(filename)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    