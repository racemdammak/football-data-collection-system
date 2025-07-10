import customtkinter as ctk
import re

event_functions = {}
SPECIAL_EVENTS = {"Corner", "Tackle", "Big Chance", "Foul", "Penalty", "Offside"}

def show_type_selection(popup, event_name, type_list, on_finish):
    for widget in popup.winfo_children():
        widget.destroy()
    label = ctk.CTkLabel(popup, text=f"Select {event_name.lower()} type(s):", font=("Segoe UI", 20, "bold"))
    label.pack(pady=(30, 20))

    var_dict = {}

    # Use a scrollable frame if the list is long (e.g. for shots)
    use_scroll = event_name.lower() == "shot" and len(type_list) > 6
    if use_scroll:
        scroll_frame = ctk.CTkScrollableFrame(popup, width=400, height=220)
        scroll_frame.pack(pady=10)
        parent = scroll_frame
    else:
        parent = popup

    # Use radio buttons for Duel, checkboxes for others
    if event_name.lower() == "duel":
        duel_var = ctk.StringVar(value=type_list[0])
        for t in type_list:
            radio = ctk.CTkRadioButton(
                parent, text=t, variable=duel_var, value=t, font=("Segoe UI", 16)
            )
            radio.pack(anchor="w", padx=60, pady=8)
        def next_page():
            show_result_page(
                popup,
                lambda result: on_finish([duel_var.get()], result),
                on_back=lambda: show_type_selection(popup, event_name, type_list, on_finish)
            )
    else:
        for t in type_list:
            var = ctk.BooleanVar()
            chk = ctk.CTkCheckBox(
                parent, text=t, variable=var, font=("Segoe UI", 16),
                checkbox_height=24, checkbox_width=24, border_width=2
            )
            chk.pack(anchor="w", padx=60, pady=8)
            var_dict[t] = var
        def next_page():
            selected_types = [k for k, v in var_dict.items() if v.get()]
            show_result_page(
                popup,
                lambda result: on_finish(selected_types, result),
                on_back=lambda: show_type_selection(popup, event_name, type_list, on_finish)
            )
    next_btn = ctk.CTkButton(
        popup, text="Next", command=next_page, fg_color="#3A6EA5", text_color="white", font=("Segoe UI", 16)
    )
    next_btn.pack(pady=40)

def show_result_page(popup, on_finish, on_back=None):
    for widget in popup.winfo_children():
        widget.destroy()
    label = ctk.CTkLabel(popup, text="Was it successful?", font=("Segoe UI", 20, "bold"))
    label.pack(pady=(40, 30))

    result_var = ctk.StringVar(value="Successful")
    success_radio = ctk.CTkRadioButton(
        popup, text="Successful", variable=result_var, value="Successful", font=("Segoe UI", 16)
    )
    unsuccess_radio = ctk.CTkRadioButton(
        popup, text="Unsuccessful", variable=result_var, value="Unsuccessful", font=("Segoe UI", 16)
    )
    success_radio.pack(pady=10)
    unsuccess_radio.pack(pady=10)

    # Place buttons directly, no frame for clean look
    btns = []
    if on_back:
        back_btn = ctk.CTkButton(
            popup, text="Back", command=on_back, fg_color="#3A6EA5", text_color="white", font=("Segoe UI", 16)
        )
        btns.append(back_btn)
    finish_btn = ctk.CTkButton(
        popup, text="Finish", command=lambda: on_finish(result_var.get()), fg_color="#41B3A2", text_color="white", font=("Segoe UI", 16)
    )
    btns.append(finish_btn)
    # Pack buttons side by side, centered below radios
    btn_frame = ctk.CTkFrame(popup, fg_color="transparent")
    btn_frame.pack(pady=30)
    for btn in btns:
        btn.pack(side="left", padx=50)

def open_event_popup(event_name):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    popup = ctk.CTkToplevel()
    popup.title(f"HeroScore - {event_name} details")
    popup.iconbitmap("logo_ico.ico")
    popup.geometry("500x500")
    popup.attributes("-topmost", True)
    popup.focus()

    def on_finish(selected_types, result):
        print(f"{event_name} types:", selected_types)
        print("Result:", result)
        popup.destroy()

    if event_name.lower() == "pass":
        show_type_selection(
            popup, "Pass",
            ["Long pass", "Short pass", "Cross", "Through ball", "Line breaking pass", "Key pass"],
            on_finish
        )
    elif event_name.lower() == "shot":
        show_type_selection(
            popup, "Shot",
            ["On target","Off target", "Blocked", "Saved by GK", "Long shot", "Close range","Header", "Free kick", "Woodwork", "Tap-in"],
            on_finish
        )
    elif event_name.lower() == "duel":
        show_type_selection(
            popup, "Duel",
            ["Ground", "Aerial"],
            on_finish
        )
    elif event_name.lower() == "dribble":
        def dribble_finish(selected_types, result):
            print(f"{event_name} types:", selected_types)
            print("Result:", result)
            popup.destroy()

        def dribble_type_selection(popup, event_name, type_list, on_finish):
            for widget in popup.winfo_children():
                widget.destroy()
            label = ctk.CTkLabel(popup, text=f"Select {event_name.lower()} type:", font=("Segoe UI", 20, "bold"))
            label.pack(pady=(30, 20))

            var_dict = {}
            for t in type_list:
                var = ctk.BooleanVar()
                chk = ctk.CTkCheckBox(
                    popup, text=t, variable=var, font=("Segoe UI", 16),
                    checkbox_height=24, checkbox_width=24, border_width=2
                )
                chk.pack(anchor="w", padx=60, pady=8)
                var_dict[t] = var

            def next_page():
                selected_types = [k for k, v in var_dict.items() if v.get()]
                if "Dribbling past opponent" in selected_types:
                    show_result_page(
                        popup,
                        lambda result: on_finish(selected_types, result),
                        on_back=lambda: dribble_type_selection(popup, event_name, type_list, on_finish)
                    )
                else:
                    # Directly finish if "Dribbled by opponent" is selected
                    on_finish(selected_types, None)

            next_btn = ctk.CTkButton(
                popup, text="Next", command=next_page, fg_color="#3A6EA5", text_color="white", font=("Segoe UI", 16)
            )
            next_btn.pack(pady=40)

        dribble_type_selection(
            popup, "Dribble",
            ["Dribbling past opponent", "Dribbled by opponent"],
            dribble_finish
        )

def special_event_func(event_name):
    open_event_popup(event_name)

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