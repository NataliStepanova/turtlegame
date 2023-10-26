from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from index_html import html

app = FastAPI()


@app.get("/")
async def get():
    return HTMLResponse(html)
