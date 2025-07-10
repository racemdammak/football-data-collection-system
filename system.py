import customtkinter as ctk
from PIL import Image
import pandas as pd
import tkinter.filedialog as fd
import tkinter.messagebox as mb
from event_popup import event_functions
from video import VideoPlayer

def open_video():
    global Video_Player
    video_path = fd.askopenfilename(filetypes=[("Video Files", "*.mp4;*.avi;*.mov;*.mkv")])
    if video_path:
        Video_Player = VideoPlayer(video_frame, video_path, width=640, height=360)

def save_events():
    match_stats = 'match\\match_stats.txt'
    match_stats_csv = 'match\\stats.csv'
    df_stats = pd.read_csv(match_stats, delimiter=',')
    df_stats.to_csv(match_stats_csv, index=False)
    mb.showinfo("Save", "Game stats have been saved successfully!")

def del_last():
    with open('match\\match_stats.txt', 'r') as file:
        lines = file.readlines()
    with open('match\\match_stats.txt', 'w') as file:
        file.writelines(lines[:-1])
    load_data()

def load_data():
    with open('match\\match_stats.txt', "r") as file:
        lines = file.readlines()
        lines = lines[-5:]
    data = [line.strip().split(",") for line in lines]
    for widget in table.winfo_children():
        widget.destroy()
    create_table(table, data)

def create_table(table, data):
    for row_index, row in enumerate(data):
        for col_index, value in enumerate(row):
            label = ctk.CTkLabel(table, text=value, width=60, height=30, text_color="white", corner_radius=5)
            label.grid(row=row_index, column=col_index, padx=5, pady=5)

def subs_player(team, player_out_entry, player_in_entry):
    player_out = player_out_entry.get()
    player_in = player_in_entry.get()
    file_path = 'match\\home_players.txt' if team == "H" else 'match\\away_players.txt'
    with open(file_path, 'r') as file:
        players = [line.strip() for line in file]
    try:
        idx = players.index(player_out)
        players[idx] = player_in
    except ValueError:
        pass
    with open(file_path, 'w') as file:
        for player in players:
            file.write(player + '\n')
    global home_players, away_players
    if team == "H":
        home_players = players
        mb.showinfo("Substitution", f"{player_out} has been substituted by {player_in} in {home_team}")
    else:
        away_players = players
        mb.showinfo("Substitution", f"{player_out} has been substituted by {player_in} in {away_team}")
    player_out_entry.delete(0, 'end')
    player_in_entry.delete(0, 'end')
    players_lists()
    window.focus_set()

def player_insertion(team, player):
    global selected_player, selected_team
    selected_player = player
    selected_team = team
    with open("match\\match_stats.txt", "a") as file:
        file.write(f"{team},{player},")

def players_lists():
    for widget in window.winfo_children():
        if isinstance(widget, ctk.CTkButton) and widget not in control_buttons:
            widget.destroy()
    y_position = 50
    for player in home_players:
        player_selection = ctk.CTkButton(window, text=player, command=lambda p=player: player_insertion(home_team, p[3:]),
                                          fg_color="white", text_color="black", hover_color="#557C56")
        player_selection.place(x=30, y=y_position)
        y_position += 50
    y_position = 50
    for player in away_players:
        player_selection = ctk.CTkButton(window, text=player, command=lambda p=player: player_insertion(away_team, p[3:]),
                                          fg_color="white", text_color="black", hover_color="#C96868")
        player_selection.place(x=200, y=y_position)
        y_position += 50

def read_team(file):
    with open(file, "r") as file:
        home_team = file.readline().strip()
        away_team = file.readline().strip()
    return home_team, away_team

def read_players(file_name):
    with open(file_name, 'r') as file:
        players = [line.strip() for line in file.readlines()]
    return players

def create_events_buttons(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()
    max_cols = 3
    btn_width = 120
    btn_height = 40
    padx = 10
    pady = 10
    num_events = len(event_functions)
    num_rows = (num_events + max_cols - 1) // max_cols
    for idx, (event_text, event_func) in enumerate(event_functions.items()):
        row = idx // max_cols
        col = idx % max_cols
        button = ctk.CTkButton(
            parent_frame,
            text=event_text,
            command=event_func,
            fg_color="#D8A25E",
            text_color="black",
            hover_color="#B99470",
            width=btn_width,
            height=btn_height
        )
        button.grid(row=row, column=col, padx=padx, pady=pady, sticky="nsew")
    for col in range(min(max_cols, num_events)):
        parent_frame.grid_columnconfigure(col, weight=1)
    for row in range(num_rows):
        parent_frame.grid_rowconfigure(row, weight=1)

def read_events(file_name):
    with open(file_name, "r") as file_events:
        events = [line.strip() for line in file_events.readlines()]
    return events

def event_insertion(event):
    with open("match\\match_stats.txt", "a") as file:
        file.write(f"{event}\n")
    #load_data()

def create_app():
    global window, home_players, away_players, home_subs, away_subs, save_btn, del_last_btn, home_team, away_team, table
    global selected_player, selected_team, events, player_in, player_out
    global video_frame, control_buttons

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    window = ctk.CTk()
    window.state('zoomed')
    window.resizable(False, False)
    window.title("HeroScore - Analyse du Match")
    window.iconbitmap("logo_ico.ico")

    # Read players and teams
    home_players = read_players('match\\home_players.txt')
    away_players = read_players('match\\away_players.txt')
    home_team, away_team = read_team('match\\team_names.txt')

    # Substitutions
    player_in = ctk.CTkEntry(window, placeholder_text='IN')
    player_in.place(x=120, y=600)
    player_out = ctk.CTkEntry(window, placeholder_text='OUT')
    player_out.place(x=120, y=635)
    home_subs = ctk.CTkButton(window, text=home_team, command=lambda: subs_player('H', player_out, player_in),
                              fg_color="#41B3A2", text_color="black", hover_color="#16423C", width=80, height=30)
    home_subs.place(x=105, y=670)
    away_subs = ctk.CTkButton(window, text=away_team, command=lambda: subs_player('A', player_out, player_in),
                              fg_color="#C7253E", text_color="black", hover_color="#821131", width=80, height=30)
    away_subs.place(x=195, y=670)

    # Events
    events_fenetre = ctk.CTkFrame(window, width=420, height=320, corner_radius=10)
    events_fenetre.place(x=360, y=40)
    global events
    events = read_events('rules\\events.txt')
    create_events_buttons(events_fenetre)

    # Video player
    video_frame = ctk.CTkFrame(window, width=650, height=380, corner_radius=10)
    video_frame.place(x=850, y=45)
    btn_x = 850
    btn_y = 10
    select_btn = ctk.CTkButton(window, text="Select Video", command=lambda:open_video(), width=110)
    select_btn.place(x=btn_x, y=btn_y)

    play_btn = ctk.CTkButton(window, text="Play", command=lambda: Video_Player.play(), width=70)
    play_btn.place(x=btn_x + 120, y=btn_y)
    pause_btn = ctk.CTkButton(window, text="Pause", command=lambda: Video_Player.pause, width=70)
    pause_btn.place(x=btn_x + 200, y=btn_y)
    speed05_btn = ctk.CTkButton(window, text="x0.5", command=lambda: Video_Player.set_speed(0.5), width=60)
    speed05_btn.place(x=btn_x + 280, y=btn_y)
    speed1_btn = ctk.CTkButton(window, text="x1", command=lambda: Video_Player.set_speed(1.0), width=60)
    speed1_btn.place(x=btn_x + 350, y=btn_y)
    speed2_btn = ctk.CTkButton(window, text="x2", command=lambda: Video_Player.set_speed(2.0), width=60)
    speed2_btn.place(x=btn_x + 420, y=btn_y)
    backward_btn = ctk.CTkButton(window, text="<< -3s", command=lambda: Video_Player.skip(-3), width=70)
    backward_btn.place(x=btn_x + 500, y=btn_y)
    forward_btn = ctk.CTkButton(window, text="+3s >>", command=lambda: Video_Player.skip(3), width=70)
    forward_btn.place(x=btn_x + 580, y=btn_y)


    # Control buttons list for exclusion in players_lists
    control_buttons = [
        home_subs, away_subs, select_btn, play_btn, pause_btn, speed05_btn, speed1_btn, speed2_btn,
        backward_btn, forward_btn
    ]
    players_lists()

    # Pitch
    pitch_fenetre = ctk.CTkFrame(window, width=540, height=340, corner_radius=10)
    pitch_fenetre.place(x=860, y=430)
    image = Image.open('football pitch.jpg')
    photo = ctk.CTkImage(image, size=(520, 320))
    pitch_label = ctk.CTkLabel(pitch_fenetre, text="", image=photo)
    pitch_label.place(relx=0.5, rely=0.5, anchor="center")

    # Table for match stats
    global table, save_btn, del_last_btn
    table = ctk.CTkFrame(window, fg_color="transparent")
    table.place(x=350, y=480)
    load_data()
    del_last_btn = ctk.CTkButton(window, text="Delete Last event", command=lambda: del_last(), fg_color="#D84040", text_color="white",
                                hover_color="#8E1616", width=80, height=30)
    del_last_btn.place(x=370, y=680)
    save_btn = ctk.CTkButton(window, text="Save Stats", command=lambda: save_events(), fg_color="#EFB036", text_color="black",
                                hover_color="#FFC785", width=80, height=30)
    save_btn.place(x=370, y=720)
    control_buttons.extend([save_btn, del_last_btn])

    window.mainloop()

# MAIN
create_app()