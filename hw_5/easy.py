import argparse
import asyncio
import pathlib
import aiofiles as aiof
import aiohttp


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--n_files', type=int, default=1, help='Number of downloaded files')
    parser.add_argument('--dir', type=str, default="artefact", help='Path to directory with downloaded files')
    return parser.parse_args()


async def load_url(filename, session):
    async with session.get(URL) as response:
        if response.status == 200:
            async with aiof.open(filename, mode='wb') as f:
                content = await response.read()
                await f.write(content)


async def loader(n_files, dir):
    async with aiohttp.ClientSession() as s:
        tasks = []
        for i in range(n_files):
            tasks.append(load_url(f"{dir}/file_{i}.png", s))
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    URL = "https://picsum.photos/200"

    args = parse_args()
    pathlib.Path(args.dir).mkdir(parents=True, exist_ok=True)
    asyncio.run(loader(args.n_files, args.dir))
