from fastapi import FastAPI
from async_retrying import retry
from fastapi_utils.tasks import repeat_every
import JSONbuilder
import logging
import json
import asyncio
import aiohttp

app = FastAPI()
logg = logging.getLogger("uvicorn.error")

categories = {}

@app.on_event("startup")
@repeat_every(seconds=60 * 6)
async def fetcherloop():
    for key in categories:
        #give room before starting a long call
        await asyncio.sleep(1)
        await start_fetching(key)
    

@retry(attempts=5)
async def fetch_category(session, url):
    async with session.get(url) as resp:
        data = await resp.json()
        if resp.status != 200 or not data:
            raise Exception('Bad data or status!')
        return data

@retry(attempts=5)
async def fetch_availability(session, url):
    async with session.get(url) as resp:
        data = await resp.json()
        if len(data['response']) <= 2 or resp.status != 200:
            raise Exception('Bad status or response missing!')
        return data

async def get_availabilities(session, brands):
    tasks = []
    for brand in brands:
        url = 'https://bad-api-assignment.reaktor.com/v2/availability/' + brand
        task = asyncio.ensure_future(fetch_availability(session, url))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results

async def get_category_full_info(session, category):
    logg.info("Fetching data for " + category)
    url = 'https://bad-api-assignment.reaktor.com/v2/products/' + category
    category_info = await fetch_category(session, url)
    brands = set()
    for i in category_info:
        brands.add(i['manufacturer'])
    availabilities = await get_availabilities(session, brands)
    logg.info("Data fetched for " + category + "! Building JSON")
    #give room between long calls
    await asyncio.sleep(1)
    return JSONbuilder.create(category_info, availabilities)

@app.get("/root")
def read_root():
    return "Select a product category for up-to-date inventory info. Please note that first-time loads might take a long time."

@app.get("/{category}")
async def read_category(category):
    if category not in categories:
        await start_fetching(category)
    return categories[category]

async def start_fetching(category):
    async with aiohttp.ClientSession() as session:
            category_full_info = await get_category_full_info(session, category)
            categories.update({category: category_full_info})