import customtkinter as ctk
from PIL import Image
import pandas as pd

def startXY(event):
    global start_x, start_y
    start_x, start_y = event.x, event.y

    with open("match\\match_stats.txt", "a") as file:
        file.write(f"{start_x},{start_y},")

def endXY(event):
    end_x, end_y = event.x, event.y

    with open("match\\match_stats.txt", "a") as file:
        file.write(f"{end_x},{end_y},")

def key_press(event):
    global key_bindings_paused
    if key_bindings_paused:
        return
    
    main_events = ["Perte de Ball", "Passe Precise", "Passe Perdue", "Longue Passe Precise", "Interception", "Dribble",
                    "Longue Passe Perdue", "Passe en Profondeur", "Tir Cadre", "Tir non Cadre"]
    key_event = event.char
    if key_event.isdigit():
        index = int(key_event)
        if 0 <= index < len(main_events):
            selected_event = main_events[index]
            insertion_event(selected_event)

def insertion_player(team, player):
    global selected_player, selected_team
    selected_player = player
    selected_team = team
    
    with open("match\\match_stats.txt", "a") as file:
        file.write(f"{team},{player},")

def insertion_event(event):
    global selected_event
    selected_event = event
    
    with open("match\\match_stats.txt", "a") as file:
        file.write(f"{event}\n")
    load_data()

def subs_player(team, player_out_entry, player_in_entry):
    player_out = player_out_entry.get()
    player_in = player_in_entry.get()

    if team == "H":
        with open('match\\home_players.txt', 'r') as file:
            data = file.read()
        data = data.replace(player_out, player_in)

        with open('match\\home_players.txt', 'w') as file:
            file.write(data)

        global home_players
        home_players = read_players('match\\home_players.txt')

    else:
        with open('match\\away_players.txt', 'r') as file:
            data = file.read()
        data = data.replace(player_out, player_in)

        with open('match\\away_players.txt', 'w') as file:
            file.write(data)

        global away_players
        away_players = read_players('match\\away_players.txt')

    player_out_entry.delete(0, 'end')
    player_in_entry.delete(0, 'end')

    fenetre.bind("<Control_L>", resume_key_bindings)

    players_lists()

def read_players(file_name):
    with open(file_name, 'r') as file:
        players = [line.strip() for line in file.readlines()]
    return players

def read_events(file_name):
    with open(file_name, "r") as file_events:
        events = [line.strip() for line in file_events.readlines()]
    return events

def read_team(file):
    with open(file, "r") as file:
        home_team = file.readline().strip()
        away_team = file.readline().strip()
    return home_team, away_team

def players_lists():
    global home_players, away_players

    for widget in fenetre.winfo_children():
        if isinstance(widget, ctk.CTkButton) and widget not in [home_subs, away_subs, save_btn, del_last_btn]:
            widget.destroy()

    y_position = 50
    for player in home_players:
        player_selection = ctk.CTkButton(fenetre, text=player, command=lambda p=player: insertion_player(home_team, p[3:]),
                                          fg_color="white", text_color="black", hover_color="#557C56")
        player_selection.place(x=30, y=y_position)
        y_position += 50

    y_position = 50
    for player in away_players:
        player_selection = ctk.CTkButton(fenetre, text=player, command=lambda p=player: insertion_player(away_team, p[3:]),
                                          fg_color="white", text_color="black", hover_color="#C96868")
        player_selection.place(x=700, y=y_position)
        y_position += 50

def resume_key_bindings(event=None):
    global key_bindings_paused
    key_bindings_paused = False
    subs_situation.configure(text="Les évenements: ON", text_color="#117554")
    fenetre.focus_set()

def disable_key_bindings(event=None):
    global key_bindings_paused
    key_bindings_paused = True
    subs_situation.configure(text="Les évenements: OFF", text_color="#C7253E")


def enable_key_bindings(event=None):
    global key_bindings_paused
    key_bindings_paused = False
    fenetre.bind("<Key>", key_press)

def save_events():
    match_stats = 'match\\match_stats.txt'
    match_stats_csv = 'match\\stats.csv'
    '''map_coordinates = 'match\\map.txt'
    map_coor_csv = 'match\\map.csv'''

    df_stats = pd.read_csv(match_stats, delimiter=',')
    df_stats.to_csv(match_stats_csv, index=False)

    '''df_map = pd.read_csv(map_coordinates, delimiter=',')
    df_map.to_csv( map_coor_csv, index=False)'''

def load_data():
    with open('match\\match_stats.txt', "r") as file:
        lines = file.readlines()
        lines = lines[-5:]

    data = [line.strip().split(",") for line in lines]
    for widget in table.winfo_children():
        widget.destroy()

    '''for col_index in range(8):
        header_label = ctk.CTkLabel(table, width=80, height=30, fg_color="#41B3A2", text_color="white", corner_radius=5)
        header_label.grid(row=0, column=col_index, padx=5, pady=5)'''

    create_table(table, data)

def create_table(table, data):
    for row_index, row in enumerate(data):
        for col_index, value in enumerate(row):
            label = ctk.CTkLabel(table, text=value, width=60, height=30, text_color="white", corner_radius=5)
            label.grid(row=row_index, column=col_index, padx=5, pady=5)

def del_last():
    with open('match\\match_stats.txt', 'r') as file:
        lines = file.readlines()

    with open('match\\match_stats.txt', 'w') as file:
        file.writelines(lines[:-1])
    load_data()

def create_app():
    global fenetre, home_players, away_players, home_subs, away_subs, save_btn, del_last_btn, home_team, away_team, table
    global selected_event, selected_player, selected_team, events, subs_situation, player_in, player_out,key_bindings_paused

    selected_event = None
    selected_player = None
    selected_team = None
    key_bindings_paused = False

    fenetre = ctk.CTk()
    fenetre.state('zoomed')
    fenetre.resizable(False, False)
    fenetre.title("HeroScore - Analyse du Match")
    fenetre.iconbitmap("logo_ico.ico")
    width = fenetre.winfo_screenwidth()
    #height = fenetre.winfo_screenheight()
    fenetre.bind("<Key>", key_press)
    
    home_players = read_players('match\\home_players.txt')
    away_players = read_players('match\\away_players.txt')
    home_team, away_team = read_team('match\\team_names.txt')

    pitch_fenetre = ctk.CTkFrame(fenetre, width=630, height=430, corner_radius=10)
    pitch_fenetre.place(x=860, y=50)
    image = Image.open('football pitch.jpg')
    photo = ctk.CTkImage(image, size=(630, 430))
    pitch_label = ctk.CTkLabel(pitch_fenetre, text="", image=photo)
    pitch_label.place(relx=0.5, rely=0.5, anchor="center")

    pitch_label.bind("<ButtonPress-1>", startXY)
    pitch_label.bind("<ButtonRelease-1>", endXY)

    events_fenetre = ctk.CTkFrame(fenetre, width=150, height=300, corner_radius=10)
    events_fenetre.place(x=180, y=50)
    events = read_events('rules\\events.txt')

    for row in range(10):
        for col in range(3):
            index = row * 3 + col
            if index < len(events):
                event_text = events[index]
                button = ctk.CTkButton(events_fenetre, text=event_text, command=lambda event=event_text: insertion_event(event[3:]),
                                       fg_color="#D8A25E", text_color="black", hover_color="#B99470")
                button.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

    
    player_in = ctk.CTkEntry(fenetre, placeholder_text='IN')
    player_in.place(x=355, y=590)
    
    player_out = ctk.CTkEntry(fenetre, placeholder_text='OUT')
    player_out.place(x=355, y=550)
    player_out.bind("<FocusIn>", disable_key_bindings)
    fenetre.bind("<Control_L>", enable_key_bindings)

    home_subs = ctk.CTkButton(fenetre, text=home_team, command=lambda: subs_player('H', player_out, player_in),
                              fg_color="#41B3A2", text_color="black", hover_color="#16423C", width=80, height=30)
    home_subs.place(x=340, y=630)
    away_subs = ctk.CTkButton(fenetre, text=away_team, command=lambda: subs_player('A', player_out, player_in),
                              fg_color="#C7253E", text_color="black", hover_color="#821131", width=80, height=30)
    away_subs.place(x=430, y=630)

    subs_situation = ctk.CTkLabel(fenetre, text="situation", font=("Arial", 14))
    subs_situation.place(x=185, y=20)
    subs_situation.configure(text="Les évenements: ON", text_color="#117554")

    table = ctk.CTkFrame(fenetre, fg_color="transparent")
    table.place(x=width - 600, y=490)

    load_data()

    save_btn = ctk.CTkButton(fenetre, text="Enregistrer", command=lambda: save_events(), fg_color="#EFB036", text_color="black",
                                hover_color="#FFC785", width=80, height=30)
    save_btn.place(x=width - 675, y=495)

    del_last_btn = ctk.CTkButton(fenetre, text="Supprimer", command=lambda: del_last(), fg_color="#D84040", text_color="white",
                                hover_color="#8E1616", width=80, height=30)
    del_last_btn.place(x=width - 675, y=530)

    players_lists()

    fenetre.mainloop()

# MAIN
create_app()