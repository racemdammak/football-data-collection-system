import customtkinter as ctk
import re

SPECIAL_EVENTS = {"Corner", "Tackle", "Big Chance", "Foul", "Penalty", "Offside"}

def open_event_popup(event_name):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    popup = ctk.CTkToplevel()
    popup.title(f"HeroScore - {event_name} details")
    popup.iconbitmap("logo_ico.ico")
    popup.geometry("500x600")
    popup.attributes("-topmost", True)
    label = ctk.CTkLabel(popup, text=f"Customize event: {event_name}", font=("Arial", 18))
    label.pack(pady=20)
    popup.focus()

def special_event_func(event_name):
    pass

def _sanitize_func_name(name):
    #Replace spaces and non-alphanumeric chars with underscores
    return re.sub(r'\W|^(?=\d)', '_', name.strip())

def _make_event_func(event_name):
    #Create a function that opens the event popup
    def event_func():
        open_event_popup(event_name)
    event_func.__name__ = _sanitize_func_name(event_name)
    return event_func

# Read events and create functions
event_functions = {}

with open("rules/events.txt", "r", encoding="utf-8") as f:
    for line in f:
        event = line.strip()
        if event:
            if event in SPECIAL_EVENTS:
                func = lambda e=event: special_event_func(e)
            else:
                func = _make_event_func(event)
            globals()[_sanitize_func_name(event)] = func  # Add to module namespace
            event_functions[event] = func     # Optional: keep a dict for lookup