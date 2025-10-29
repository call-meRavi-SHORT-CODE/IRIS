import os
from langgraph.prebuilt import create_react_agent
from langchain.tools import tool
from typing import Any, Dict
from typing import List, Literal
from langchain_google_genai import ChatGoogleGenerativeAI
from tools import open_google,open_youtube,open_notepad,open_calculator,close_browser,open_file_explorer,open_settings
from tools import open_task_manager, open_microsoft_store,open_word,open_ppt,open_excel,close_application
from tools import set_brightness,take_screenshot,volume_down,volume_up,mute
from prompts import system_prompt


#from config import api_key

os.environ.setdefault("USER_AGENT", "IRIS")
os.environ["PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION"] =  "python"

GOOGLE_API_KEY = "AIzaSyAnPL4zvdny1jVeaikGJZz4JDL_5q11aSA"

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=GOOGLE_API_KEY)


tools = [open_google,open_calculator,open_notepad,open_youtube,close_browser,open_file_explorer,open_settings,open_task_manager, open_microsoft_store,open_word,open_ppt,open_excel,close_application,set_brightness,take_screenshot,volume_down,volume_up,mute]


IRIS = create_react_agent(model=llm,tools=tools,prompt=system_prompt)

def run_agent(question: str):
    inputs = {"messages": [("user", question)]}
    for step in IRIS.stream(inputs, stream_mode="values"):
        msg = step['messages'][-1]
        msg.pretty_print()

if __name__ == "__main__":
    run_agent("IRIS volume up")