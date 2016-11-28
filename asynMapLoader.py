import asyncio
import aiohttp
import async_timeout
import tqdm
import os

async def download_coroutine(session, url, fname):
    sem = asyncio.Semaphore(20)
    async with sem:
        with async_timeout.timeout(10):
            if os.path.exists(str(fname)+".png"):
                return
            async with session.get(url) as response:
                filename = str(fname)+".png"
                with open(filename, 'wb') as f_handle:
                    while True:
                        chuck = await response.content.read(1024)
                        if not chuck:
                            break
                        f_handle.write(chuck)
                return await response.release()


async def download(loop, urllist, d_desc):
    '''
        :param loop:
        :param urllist:
        :return null:
    '''
    async with aiohttp.ClientSession(loop=loop) as session:
        for (key, val) in tqdm.tqdm(urllist.items(), desc=d_desc, total=len(urllist)):
            await download_coroutine(session, val, key)


def main(downloadList, d_desc):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(download(loop, downloadList, d_desc))


if __name__ == '__main__':
    main("test")