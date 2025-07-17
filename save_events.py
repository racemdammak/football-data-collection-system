selected_team = None
selected_player = None
selected_event_name = None  # Main event (e.g. Pass, Shot)
selected_event = None        # Subtype (e.g. Short pass, On target)
selected_result = None       # "Successful", "Unsuccessful", or None
start_x = None
start_y = None
end_x = None
end_y = None
table_widget = None

def set_table_widget(widget):
    global table_widget
    table_widget = widget

def set_event(event_name, event_type, result):
    with open("match\\match_stats.txt", "a", encoding="utf-8") as file:
        file.write(f"{event_name},{event_type},{result},")
    load_data()

def insertion_player(team, player):
    with open("match\\match_stats.txt", "a", encoding="utf-8") as file:
        file.write(f"\n{team},{player},")

def startXY(event):
    start_x, start_y = event.x, event.y
    with open("match\\match_stats.txt", "a", encoding="utf-8") as file:
        file.write(f"{start_x},{start_y},")

def endXY(event):
    end_x, end_y = event.x, event.y
    with open("match\\match_stats.txt", "a", encoding="utf-8") as file:
        file.write(f"{end_x},{end_y}")
    load_data()

def load_data():
    if table_widget is None:
        return
    with open('match\\match_stats.txt', "r", encoding="utf-8") as file:
        lines = [line.strip() for line in file if line.strip()]
    last_lines = lines[-5:]
    data = [line.split(",") for line in last_lines]
    for widget in table_widget.winfo_children():
        widget.destroy()
    for row_index, row in enumerate(data):
        for col_index, value in enumerate(row):
            from customtkinter import CTkLabel
            label = CTkLabel(table_widget, text=value, width=60, height=30, text_color="white", corner_radius=5)
            label.grid(row=row_index, column=col_index, padx=5, pady=5)