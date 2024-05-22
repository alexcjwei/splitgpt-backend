from typing import List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from lib.chains import MarkdownTable, extract_contributions_chain

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://yourfrontenddomain.com",
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
    return FillTableResponse(
        columns=["People", "Dinner", "Drinks"],
        data=[["Alice", 10.00, 5.00], ["Bob", 0.00, 10.00]],
    )
    table: MarkdownTable = extract_contributions_chain.invoke({"input": req.text})
    return FillTableResponse(columns=table.header, data=table.data)
