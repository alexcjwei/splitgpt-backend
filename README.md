# Backend

Built with FastAPI and LangChain.

## Features
- Single POST endpoint `/create-contributions-table`, which takes text and returns the table data for the frontend
- A 3-step chain which first lists purchase data as text, then formats that list into a Markdown table, and finally extracts that Markdown table into structured format to respond with.


## Installation

```shell
pip install -r requirements.txt
fastapi dev main.py
```


