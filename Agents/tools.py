import webbrowser
from langchain.tools import tool
import os
import pyautogui
import time
import wmi


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


# Tool to open File Explorer
@tool
def open_file_explorer() -> str:
    """Opens File Explorer."""
    try:
        os.system("start explorer")
        return "IRIS <-- Opening File Explorer..."
    except Exception as e:
        return f"Failed to open File Explorer: {str(e)}"

# Tool to open Windows Settings
@tool
def open_settings() -> str:
    """Opens Windows Settings."""
    try:
        os.system("start ms-settings:")
        return "IRIS <-- Opening Settings..."
    except Exception as e:
        return f"Failed to open Settings: {str(e)}"

# Tool to open Task Manager
@tool
def open_task_manager() -> str:
    """Opens Task Manager."""
    try:
        os.system("taskmgr")
        return "IRIS <-- Opening Task Manager..."
    except Exception as e:
        return f"Failed to open Task Manager: {str(e)}"

# Tool to open Microsoft Store
@tool
def open_microsoft_store() -> str:
    """Opens Microsoft Store."""
    try:
        os.system("start ms-store:")
        return "IRIS <-- Opening Microsoft Store..."
    except Exception as e:
        return f"Failed to open Microsoft Store: {str(e)}"

# Tool to open Microsoft Word
@tool
def open_word() -> str:
    """Opens Microsoft Word."""
    try:
        os.system("start winword")
        return "IRIS <-- Opening Microsoft Word..."
    except Exception as e:
        return f"Failed to open Microsoft Word: {str(e)}"

# Tool to open Microsoft PowerPoint
@tool
def open_ppt() -> str:
    """Opens PowerPoint."""
    try:
        os.system("start powerpnt")
        return "IRIS <-- Opening PowerPoint..."
    except Exception as e:
        return f"Failed to open PowerPoint: {str(e)}"

# Tool to open Microsoft Excel
@tool
def open_excel() -> str:
    """Opens Excel."""
    try:
        os.system("start excel")
        return "IRIS <-- Opening Excel..."
    except Exception as e:
        return f"Failed to open Excel: {str(e)}"

# Tool to close an application (e.g., Word, Excel)
@tool
def close_application(application_name: str) -> str:
    """Closes a specified application by name."""
    try:
        os.system(f'taskkill /f /im {application_name}')
        return f"IRIS <-- Closing {application_name}..."
    except Exception as e:
        return f"Failed to close {application_name}: {str(e)}" 

# Tool to set screen brightness
@tool
def set_brightness(brightness_level: int) -> str:
    """Sets the screen brightness."""
    try:
        c = wmi.WMI(namespace='wmi')
        methods = c.WmiMonitorBrightnessMethods()[0]
        methods.WmiSetBrightness(brightness_level, 0)
        return f"IRIS <-- Setting brightness to {brightness_level}%"
    except Exception as e:
        return f"Failed to set brightness: {str(e)}"

# Tool to take a screenshot and save it with a specified filename
@tool
def take_screenshot(filename: str) -> str:
    """Takes a screenshot and saves it with a specified filename."""
    try:
        time.sleep(3)  # Allow for a short delay
        screenshot = pyautogui.screenshot()
        screenshot.save(f'{filename}.png')
        return f"IRIS <-- Screenshot saved as {filename}.png"
    except Exception as e:
        return f"Failed to take screenshot: {str(e)}"

# Tool to control volume (volume up)
@tool
def volume_up() -> str:
    """Increases the system volume."""
    try:
        for _ in range(10):  # Repeat volume up command multiple times
            pyautogui.press("volumeup")
        return "IRIS <-- Volume increased."
    except Exception as e:
        return f"Failed to increase volume: {str(e)}"

# Tool to control volume (volume down)
@tool
def volume_down() -> str:
    """Decreases the system volume."""
    try:
        for _ in range(10):  # Repeat volume down command multiple times
            pyautogui.press("volumedown")
        return "IRIS <-- Volume decreased."
    except Exception as e:
        return f"Failed to decrease volume: {str(e)}"

# Tool to mute the system volume
@tool
def mute() -> str:
    """Mutes the system volume."""
    try:
        pyautogui.press("volumemute")
        return "IRIS <-- Volume muted."
    except Exception as e:
        return f"Failed to mute volume: {str(e)}"