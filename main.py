import customtkinter as ctk
from subprocess import call
import os

def save_home_players(entries):
    global home_lock
    home_players = [entry.get() for entry in entries]
    for name in home_players:
        if name == "":
            message_label_h.configure(text="Error!", fg_color="red")
        else:
            message_label_h.configure(text="Players saved!", fg_color="green")

        with open('match\\home_players.txt', 'w') as file:
            for player in home_players:
                file.write(player+'\n')
    home_lock = 1

def save_away_players(entries):
    global away_lock
    away_players = [entry.get() for entry in entries]
    for name in away_players:
        if name == "":
            message_label_a.configure(text="Error!", fg_color="red")
        else:
            message_label_a.configure(text="Players saved!", fg_color="green")

        with open('match\\away_players.txt', 'w') as file:
            for player in away_players:
                file.write(player+'\n')
    away_lock = 1

def home_page(fenetre):
    width = fenetre.winfo_screenwidth()

    group_distance = 300
    group_width = 100
    center_x = width // 2

    home_x = center_x - group_distance // 2 - group_width // 2
    away_x = center_x + group_distance // 2 - group_width // 2

    # HOME TEAM
    label = ctk.CTkLabel(fenetre, text="HOME", fg_color="transparent")
    label.place(x=home_x + 50, y=10)

    positions = 1
    home_players = []
    y_position = 50

    for i in range(11):
        player_entry = ctk.CTkEntry(fenetre, placeholder_text=positions)
        positions += 1
        player_entry.place(x=home_x, y=y_position)
        home_players.append(player_entry)
        y_position += 50

    home_players_btn = ctk.CTkButton(fenetre, text="Save", command=lambda: save_home_players(home_players))
    y_position_1 = y_position + 10
    home_players_btn.place(x=home_x, y=y_position_1)

    global message_label_h
    message_label_h = ctk.CTkLabel(fenetre, text="", fg_color="transparent")
    message_label_h.place(x=home_x, y=y_position_1 + 50)

    # AWAY TEAM
    away_label = ctk.CTkLabel(fenetre, text="AWAY", fg_color="transparent")
    away_label.place(x=away_x + 50, y=10)
    positions_away = 1
    away_players = []
    y_position_away = 50

    for i in range(11):
        away_player_entry = ctk.CTkEntry(fenetre, placeholder_text=positions_away)
        positions_away += 1
        away_player_entry.place(x=away_x, y=y_position_away)
        away_players.append(away_player_entry)
        y_position_away += 50

    away_players_btn = ctk.CTkButton(fenetre, text="Save", command=lambda: save_away_players(away_players))
    y_position_2 = y_position_away + 10
    away_players_btn.place(x=away_x, y=y_position_2)

    global message_label_a
    message_label_a = ctk.CTkLabel(fenetre, text="", fg_color="transparent")
    message_label_a.place(x=away_x, y=y_position_2 + 50)

    # Enter Teams Name (top left)
    entry_x = 50
    labelentryHOME = ctk.CTkEntry(fenetre, placeholder_text="HOME")
    labelentryHOME.place(x=entry_x, y=30)
    labelentryAWAY = ctk.CTkEntry(fenetre, placeholder_text="AWAY")
    labelentryAWAY.place(x=entry_x, y=70)

    # Save team names to a file
    def save_team_names():
        global home_name_lock, away_name_lock
        home_team = labelentryHOME.get()
        away_team = labelentryAWAY.get()
        if home_team == '' or away_team == '':
            message_label.configure(text="Error!", fg_color="red")
        else:
            with open('match\\team_names.txt', 'w') as f:
                f.write(f"{home_team}\n{away_team}")
                message_label.configure(text="Teams saved", fg_color="green")
        home_name_lock = 1
        away_name_lock = 1

    global message_label
    message_label = ctk.CTkLabel(fenetre, text="", fg_color="transparent")
    message_label.place(x=entry_x, y=150)

    save_team_names_btn = ctk.CTkButton(fenetre, text="Save Teams", command=lambda: save_team_names())
    save_team_names_btn.place(x=entry_x, y=110)

def match_interface(fenetre):
    if (home_lock and away_lock and home_name_lock and away_name_lock) == True:
        fenetre.destroy()

        def open_analysis_interface():
            call(["python", "match.py"])

        open_analysis_interface()
    os.startfile('match.exe')
def create_app():
    global home_lock, away_lock, home_name_lock, away_name_lock
    home_lock, away_lock, home_name_lock, away_name_lock = 0, 0, 0, 0
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")

    fenetre = ctk.CTk()
    fenetre.state('zoomed')
    fenetre.resizable(False, False)
    fenetre.title("HersoScore")
    fenetre.iconbitmap("logo_ico.ico")

    # Create home page
    home_page(fenetre)

    # Go to match interface
    width = fenetre.winfo_screenwidth()
    height = fenetre.winfo_screenheight()
    start_game_btn = ctk.CTkButton(fenetre, text="Start Match", command=lambda: match_interface(fenetre))
    start_game_btn.place(x=(width//2) - 50, y=height - 175)

    fenetre.mainloop()
    
#MAIN
create_app()
