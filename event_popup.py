import customtkinter as ctk
import re
import save_events as se

event_functions = {}
SPECIAL_EVENTS = {"Corner", "Tackle", "Assist", "Interception", "Clearance", "Big Chance", "Foul", "Penalty", "Offside"}

def show_type_selection(popup, event_name, type_list, on_finish):
    for widget in popup.winfo_children():
        widget.destroy()
    label = ctk.CTkLabel(popup, text=f"Select {event_name.lower()} type(s):", font=("Segoe UI", 20, "bold"))
    label.pack(pady=(30, 20))
    var_dict = {}
    parent = popup
    if event_name.lower() == "duel":
        duel_var = ctk.StringVar(value=type_list[0])
        for t in type_list:
            radio = ctk.CTkRadioButton(parent, text=t, variable=duel_var, value=t, font=("Segoe UI", 16))
            radio.pack(anchor="w", padx=60, pady=8)
        def next_page():
            show_result_page(popup, lambda result: on_finish([duel_var.get()], result), on_back=lambda: show_type_selection(popup, event_name, type_list, on_finish))
    else:
        for t in type_list:
            var = ctk.BooleanVar()
            chk = ctk.CTkCheckBox(parent, text=t, variable=var, font=("Segoe UI", 16), checkbox_height=24, checkbox_width=24, border_width=2)
            chk.pack(anchor="w", padx=60, pady=8)
            var_dict[t] = var
        def next_page():
            selected_types = [k for k, v in var_dict.items() if v.get()]
            show_result_page(popup, lambda result: on_finish(selected_types, result), on_back=lambda: show_type_selection(popup, event_name, type_list, on_finish))
    ctk.CTkButton(popup, text="Next", command=next_page, fg_color="#3A6EA5", text_color="white", font=("Segoe UI", 16)).pack(pady=40)

def show_result_page(popup, on_finish, on_back=None):
    for widget in popup.winfo_children():
        widget.destroy()
    label = ctk.CTkLabel(popup, text="Was it successful?", font=("Segoe UI", 20, "bold"))
    label.pack(pady=(40, 30))
    result_var = ctk.StringVar(value="Successful")
    ctk.CTkRadioButton(popup, text="Successful", variable=result_var, value="Successful", font=("Segoe UI", 16)).pack(pady=10)
    ctk.CTkRadioButton(popup, text="Unsuccessful", variable=result_var, value="Unsuccessful", font=("Segoe UI", 16)).pack(pady=10)
    btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
    btn_frame.pack(pady=30)
    if on_back:
        ctk.CTkButton(btn_frame, text="Back", command=on_back, fg_color="#3A6EA5", text_color="white", font=("Segoe UI", 16)).pack(side="left", padx=50)
    ctk.CTkButton(btn_frame, text="Finish", command=lambda: on_finish(result_var.get()), fg_color="#41B3A2", text_color="white", font=("Segoe UI", 16)).pack(side="left", padx=50)

def open_event_popup(event_name):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    popup = ctk.CTkToplevel()
    popup.title(f"HeroScore - {event_name} details")
    popup.iconbitmap("logo_ico.ico")
    popup.geometry("500x500")
    popup.attributes("-topmost", True)
    popup.focus()
    def save_and_close(selected_types, result=None):
        se.set_event(event_name, selected_types[0] if selected_types else None, result if result is not None else "None")
        popup.destroy()
    if event_name.lower() == "pass":
        show_type_selection(popup, "Pass", ["Short pass", "Long pass", "Cross", "Through ball", "Line breaking pass", "Key pass"], save_and_close)
    elif event_name.lower() == "shot":
        show_single_choice_page(popup, "Shot", ["On target", "Off target", "Blocked", "Saved by GK", "Header", "Free kick", "Woodwork", "Tap-in"], save_and_close)
    elif event_name.lower() == "duel":
        show_type_selection(popup, "Duel", ["Ground", "Aerial"], save_and_close)
    elif event_name.lower() == "dribble":
        def dribble_type_selection(popup, event_name, type_list, on_finish):
            for widget in popup.winfo_children():
                widget.destroy()
            label = ctk.CTkLabel(popup, text=f"Select {event_name.lower()} type:", font=("Segoe UI", 20, "bold"))
            label.pack(pady=(30, 20))
            var_dict = {}
            for t in type_list:
                var = ctk.BooleanVar()
                chk = ctk.CTkCheckBox(popup, text=t, variable=var, font=("Segoe UI", 16), checkbox_height=24, checkbox_width=24, border_width=2)
                chk.pack(anchor="w", padx=60, pady=8)
                var_dict[t] = var
            def next_page():
                selected_types = [k for k, v in var_dict.items() if v.get()]
                if "Dribbling past opponent" in selected_types:
                    show_result_page(popup, lambda result: on_finish(selected_types, result), on_back=lambda: dribble_type_selection(popup, event_name, type_list, on_finish))
                else:
                    on_finish(selected_types, None)
            ctk.CTkButton(popup, text="Next", command=next_page, fg_color="#3A6EA5", text_color="white", font=("Segoe UI", 16)).pack(pady=40)
        dribble_type_selection(popup, "Dribble", ["Dribbling past opponent", "Dribbled by opponent"], save_and_close)
    elif event_name.lower() == "goalkeeper actions":
        show_type_selection(popup, "Goalkeeper Actions", ["Save", "High claim", "Short hand pass", "Long hand pass"], save_and_close)
    elif event_name.lower() == "cards":
        show_single_choice_page(popup, "Cards", ["Yellow", "Red"], save_and_close)
    elif event_name.lower() == "loss of ball":
        show_single_choice_page(popup, "Loss of ball", ["Under pressure", "No pressure"], save_and_close)
    elif event_name.lower() == "goal":
        show_single_choice_page(popup, "Goal", ["Goal", "Own-Goal"], save_and_close)

def special_event_func(event_name):
    se.set_special_event(event_name)

def _sanitize_func_name(name):
    return re.sub(r'\W|^(?=\d)', '_', name.strip())

def _make_event_func(event_name):
    def event_func():
        open_event_popup(event_name)
    event_func.__name__ = _sanitize_func_name(event_name)
    return event_func

with open("rules/events.txt", "r", encoding="utf-8") as f:
    for line in f:
        event = line.strip()
        if event:
            if event in SPECIAL_EVENTS:
                func = lambda e=event: special_event_func(e)
            else:
                func = _make_event_func(event)
            globals()[_sanitize_func_name(event)] = func
            event_functions[event] = func

def show_single_choice_page(popup, event_name, options, on_finish):
    for widget in popup.winfo_children():
        widget.destroy()
    label = ctk.CTkLabel(popup, text=f"Select {event_name.lower()} type:", font=("Segoe UI", 20, "bold"))
    label.pack(pady=(30, 20))
    choice_var = ctk.StringVar(value=options[0])
    parent = ctk.CTkScrollableFrame(popup, width=400, height=220) if len(options) > 6 else popup
    if len(options) > 6:
        parent.pack(pady=10)
    for opt in options:
        radio = ctk.CTkRadioButton(parent, text=opt, variable=choice_var, value=opt, font=("Segoe UI", 16))
        radio.pack(anchor="w", padx=60, pady=8)
    def next_page():
        selected_types = [choice_var.get()]
        on_finish(selected_types, None)
    ctk.CTkButton(popup, text="Finish", command=next_page, fg_color="#3A6EA5", text_color="white", font=("Segoe UI", 16)).pack(pady=40)