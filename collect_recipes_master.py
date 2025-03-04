import aiohttp
import asyncio

# import proxies 
proxy_list = []
with open("working_proxies.txt") as file:
    for line in file:
        proxy_list.append(line)





urls = ["https://example.com", "https://example.org"]

async def fetch(session, url):
    async with session.get(url) as response:
        return await response.text()[:100]

async def main():
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        results = await asyncio.gather(*tasks)  # Runs all requests concurrently
        print(results)

asyncio.run(main())
