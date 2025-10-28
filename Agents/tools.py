import webbrowser
from langchain.tools import tool



@tool
def open_google() -> str:
    """Opens Google in the default web browser."""
    try:
        webbrowser.open("https://www.google.com")
        return "IRIS <-- Opening Google..."
    except Exception as e:
        return f"Failed to open Google: {str(e)}"