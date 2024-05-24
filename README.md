# Backend

Built with FastAPI and LangChain + OpenAI's ChatGPT3.5 API.  Deployed on Heroku.

Live on Vercel: https://splitgpt-alexwei.vercel.app/

Frontend: https://github.com/alexcjwei/splitgpt-frontend

## Features

- Single POST endpoint `/create-contributions-table`, which takes text and returns the table data for the frontend
- A 3-step chain which first lists purchase data as text, then formats that list into a Markdown table, and finally extracts that Markdown table into structured format to respond with.
- Also an input validation chain to make sure people aren't submitting random nonsense


## Installation

```shell
pip install -r requirements.txt
fastapi dev main.py
```


