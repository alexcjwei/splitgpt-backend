from langchain_core.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.pydantic_v1 import BaseModel, Field, conlist
from typing import List
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-0125")

list_contributions_prompt = ChatPromptTemplate.from_template(
    """Extract the contributions made by each person from the following prompt.
A contribution is an amount of money contributed towards an expense or purchase.

Passage:

{input}

Output format:

<Name 1>: <Item 1> ($<Item 1 cost>), ...

Replace the brackets with the names of people, the items they contributed to, and their cost.
If the cost is not explicitly mentioned, leave as $0. 
If the passage refers to oneself like with "I" or "me", use "You" as the name.
Do not hallucinate any information, only extract what is explicitly mentioned.
"""
)
list_contributions_chain = list_contributions_prompt | llm | StrOutputParser()


tablify_contributions_prompt = ChatPromptTemplate.from_template(
    """Extract the contributions made by each person
into a Markdown table. The table header should be a list of "People" followed by item names.
Each row of data starts with a person's name, and indicates how much they contributed to an item.
If a person did not contribute to a purchase, use `$0` as the value for the cell.
Do not hallucinate any information, only extract what is explicitly mentioned.

Contributions:

{input}
"""
)
tablify_contributions_chain = tablify_contributions_prompt | llm | StrOutputParser()


class MarkdownTable(BaseModel):
    """A Markdown Table described as a header and a list of data"""

    header: List[str] = Field("The table header row")
    data: List[conlist(float | str)] = Field(  # type: ignore
        "A list of rows, with the first value a string and following values floats"
    )


extract_to_table_format_prompt = ChatPromptTemplate.from_template(
    """Extract information from this Markdown table.

Only extract the properties mentioned in the 'MarkdownTable' function.
Extract money values as floats and text as string.
This means if you see "$5", you should pass something like `5.00`.
Do not hallucinate any information, only extract what is explicitly mentioned.

Markdown table:
```
{input}
```
"""
)
extract_to_table_format_chain = (
    extract_to_table_format_prompt | llm.with_structured_output(MarkdownTable)
)


extract_contributions_chain = (
    list_contributions_chain
    | tablify_contributions_chain
    | extract_to_table_format_chain
)

check_valid_input_chain = (
    ChatPromptTemplate.from_template(
        """Check if the text below is a description of purchases made.
Respond yes if so and no otherwise.
    
Passage:
{input}

Ouptut format:
yes OR no
"""
    )
    | llm
    | StrOutputParser()
)
