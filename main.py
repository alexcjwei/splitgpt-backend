from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
from lib.chains import (
    MarkdownTable,
    extract_contributions_chain,
    check_valid_input_chain,
)

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://sharegpt-frontend.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Origins that are allowed to make requests
    allow_credentials=True,  # Allow cookies to be sent in cross-origin requests
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


class ExtractInfoRequest(BaseModel):
    text: str


class FillTableRequest(BaseModel):
    text: str


class FillTableResponse(BaseModel):
    columns: List[str]
    data: List[List[str | float]]


@app.post("/create-contributions-table")
def fill_table(req: FillTableRequest):
    is_valid: str = check_valid_input_chain.invoke({"input": req.text})

    if is_valid.lower().startswith("n"):
        raise HTTPException(
            status_code=400,
            detail="Not a valid description. Please describe who made which purchases for how much, and try again.",
        )

    table: MarkdownTable = extract_contributions_chain.invoke({"input": req.text})
    print(table)
    return FillTableResponse(columns=table.header, data=table.data)
