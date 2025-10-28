import webbrowser
from langchain.tools import tool
import os


@tool
def open_google() -> str:
    """Opens Google in the default web browser."""
    try:
        webbrowser.open("https://www.google.com")
        return "IRIS <-- Opening Google..."
    except Exception as e:
        return f"Failed to open Google: {str(e)}"


@tool
def open_youtube(query: str) -> str:
    """Plays a query on YouTube."""
    try:
        webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
        return f"IRIS <-- Playing {query} on YouTube..."
    except Exception as e:
        return f"Failed to play {query} on YouTube: {str(e)}"

# Tool to close browser (Microsoft Edge in this case)
@tool
def close_browser() -> str:
    """Closes the browser."""
    try:
        os.system('taskkill /f /im msedge.exe')
        return "IRIS <-- Closing the browser..."
    except Exception as e:
        return f"Failed to close browser: {str(e)}"

# Tool to open Notepad
@tool
def open_notepad() -> str:
    """Opens Notepad."""
    try:
        os.system("start notepad")
        return "IRIS <-- Opening Notepad..."
    except Exception as e:
        return f"Failed to open Notepad: {str(e)}"

# Tool to open Calculator
@tool
def open_calculator() -> str:
    """Opens Calculator."""
    try:
        os.system("start calc")
        return "IRIS <-- Opening Calculator..."
    except Exception as e:
        return f"Failed to open Calculator: {str(e)}"
