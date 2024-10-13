from typing import Annotated

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import HTMLResponse

from authorization import checkAuthorization, AuthorizationError
from mdict_query import IndexBuilder
from mdx_util import get_definition_mdx

builder = IndexBuilder("./vocabulary.com/vocabulary.com.mdx")
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/{word}")
async def vocabulary(
    word: str,
    authorization: Annotated[str | None, Header()] = None,
):
    try:
        checkAuthorization(authorization)
    except AuthorizationError as e:
        raise HTTPException(status_code=e.status_code, detail=e.detail)
    content = get_definition_mdx(word, builder)[0]
    return HTMLResponse(content=content, status_code=200)
