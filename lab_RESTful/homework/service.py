import aiohttp
import asyncio
import json


from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()
WF_API_KEY = "39e4020d73124a78aadbcba786976e8d"
ST_API_KEY = "5UMPCZzxxrw4mg-eAITbrpmm80LVx0JH"
endpoints = []

whois_urls = []


async def mock_tasks(session: aiohttp.ClientSession):
    tasks = []
    for endpoint in endpoints:
        tasks.append(session.get(endpoint.format( )))


@app.get('/')
async def get_page():
    return FileResponse("index.html", media_type="text/html") 


@app.get("/report")
async def get_report(domain_name: str):
    results = []
    async with aiohttp.ClientSession() as session:
        tasks = mock_tasks(session)
        responses = await asyncio.gather(*tasks)
        for response in responses():
            results.append(await response.json())








# conn = http.client.HTTPSConnection("api.whoisfreaks.com")
#     payload = ''
#     headers = {}
#     print(f"GET", "/v1.0/whois?whois=live&domainName={domain_name}&apiKey={API_KEY}")
#     conn.request(
#         "GET",
#         f"/v1.0/whois?whois=live&domainName={domain_name}&apiKey={API_KEY}",
#         payload,
#         headers)
    
#     res = conn.getresponse()
#     data = json.loads(res.read().decode("utf-8"))
#     print(data)
#     return {"message": data}