import os
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from typing import Any, Dict
from typing import List, Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import open_google
from prompts import system_prompt


#from config import api_key

os.environ.setdefault("USER_AGENT", "IRIS")
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] =  "python"

GOOGLE_API_KEY = "AIzaSyAnPL4zvdny1jVeaikGJZz4JDL_5q11aSA"

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)


tools = [open_google]


IRIS = create_react_agent(model=llm,tools=tools,prompt=system_prompt)

def run_agent(question: str):
    inputs = {"messages": [("user", question)]}
    for step in IRIS.stream(inputs, stream_mode="values"):
        msg = step['messages'][-1]
        msg.pretty_print()

if __name__ == "__main__":
    run_agent("open google")