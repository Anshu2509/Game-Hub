import json
import os
import random
import time
import turtle
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
# ==============================================================================
# SECTION 1: BACKEND LOGIC (ACCOUNT & GAME MANAGEMENT)
# This logic remains unchanged.
# ==============================================================================
DATA_FILE = 'player_data.json'
def load_data():
    if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
        return {}
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)
def register_user(username, password):
    if not username: return False, "Username cannot be empty."
    if not password: return False, "Password cannot be empty."
    data = load_data()
    if username in data: return False, "Username already exists!"
    data[username] = {"password": password, "scores": {"game1_number_guess": "Not Played", "game2_rps": "Not Played", "game3_snake": "Not Played"}}
    save_data(data)
    return True, "Account created successfully!"
def login_user(username, password):
    data = load_data()
    if username in data and data[username]['password'] == password:
        return True
    else:
        return False
def update_score(username, game_id, score):
    data = load_data()
    if username not in data: return "Error updating score."
    current_scores = data[username]['scores']
    message = ""
    if game_id == "game3_snake":
        current_high = current_scores.get(game_id, 0) if isinstance(current_scores.get(game_id), int) else 0
        if score > current_high:
            current_scores[game_id] = score
            message = f"🎉 New high score for Snake: {score}!"
        else:
            message = f"Your score: {score}. High score: {current_high}."
    elif game_id == "game1_number_guess":
        current_best = current_scores.get(game_id, float('inf')) if isinstance(current_scores.get(game_id), int) else float('inf')
        if current_best == "Not Played" or score < current_best:
            current_scores[game_id] = score
            message = f"🎉 New best score for Number Guessing: {score} attempts!"
        else:
            message = f"Your score: {score}. Best score: {current_best}."
    else:
        current_scores[game_id] = score
        message = "Score saved!"
    save_data(data)
    return message
def get_player_scores_display(username):
    data = load_data()
    if username in data:
        scores = data[username]['scores']
        return (f"--- 🏆 Scores for {username} ---\n\n"
                f"Number Guessing Best: {scores.get('game1_number_guess', 'N/A')} attempts\n"
                f"Rock Paper Scissors Wins:  {scores.get('game2_rps', 'N/A')}\n"
                f"Snake Game High Score: {scores.get('game3_snake', 'N/A')}")
    return "Could not find scores for this user."
# ==============================================================================
# SECTION 2: GAME LOGIC
# This logic remains unchanged.
# ==============================================================================
def play_number_guessing_game():
    secret_number = random.randint(1, 100)
    attempts = 0
    messagebox.showinfo("Number Guessing", "I'm thinking of a number between 1 and 100.")
    while True:
        guess_str = simpledialog.askstring("Guess", "Enter your guess:")
        if guess_str is None: return "Cancelled"
        if not guess_str.isdigit():
            messagebox.showerror("Error", "Please enter a number.")
            continue
        guess = int(guess_str)
        attempts += 1
        if guess < secret_number: messagebox.showinfo("Result", "Too low!")
        elif guess > secret_number: messagebox.showinfo("Result", "Too high!")
        else:
            messagebox.showinfo("Correct!", f"You guessed the number in {attempts} attempts.")
            return attempts
def play_rps_game():
    options = ['rock', 'paper', 'scissors']
    player_score = 0
    for i in range(3):
        player_choice = simpledialog.askstring(f"Round {i+1}", "Choose rock, paper, or scissors:").lower()
        if player_choice is None: return "Cancelled"
        if player_choice not in options:
            messagebox.showerror("Invalid", "Invalid choice. This round is forfeit.")
            continue
        computer_choice = random.choice(options)
        result = ""
        if player_choice == computer_choice: result = "It's a tie!"
        elif (player_choice == 'rock' and computer_choice == 'scissors') or \
             (player_choice == 'scissors' and computer_choice == 'paper') or \
             (player_choice == 'paper' and computer_choice == 'rock'):
            result = "You win this round!"; player_score += 1
        else: result = "Computer wins this round!"
        messagebox.showinfo(f"Round {i+1} Result", f"You chose {player_choice}, computer chose {computer_choice}.\n\n{result}")
    return player_score
def play_snake_game():
    try:
        wn = turtle.Screen()
        wn.title("Snake Game"); wn.bgcolor("black"); wn.setup(width=600, height=600); wn.tracer(0)
    except turtle.Terminator:
        turtle.TurtleScreen._RUNNING = True
        wn = turtle.Screen(); wn.title("Snake Game"); wn.bgcolor("black"); wn.setup(width=600, height=600); wn.tracer(0)
    
    head = turtle.Turtle(); head.shape("square"); head.color("green"); head.penup(); head.goto(0,0); head.direction = "stop"
    food = turtle.Turtle(); food.shape("circle"); food.color("red"); food.penup(); food.goto(0,100)
    pen = turtle.Turtle(); pen.hideturtle(); pen.speed(0); pen.shape("square"); pen.color("white"); pen.penup(); pen.goto(0, 260)
    pen.write("Score: 0", align="center", font=("Courier", 24, "normal"))
    segments = []; score = 0; delay = 0.1; session_high_score = 0
    def go_up():
        if head.direction != "down": head.direction = "up"
    def go_down():
        if head.direction != "up": head.direction = "down"
    def go_left():
        if head.direction != "right": head.direction = "left"
    def go_right():
        if head.direction != "left": head.direction = "right"
    def move():
        if head.direction == "up": head.sety(head.ycor() + 20)
        if head.direction == "down": head.sety(head.ycor() - 20)
        if head.direction == "left": head.setx(head.xcor() - 20)
        if head.direction == "right": head.setx(head.xcor() + 20)
    wn.listen()
    wn.onkeypress(go_up, "Up"); wn.onkeypress(go_down, "Down"); wn.onkeypress(go_left, "Left"); wn.onkeypress(go_right, "Right")
    
    try:
        while True:
            game_over = False
            while not game_over:
                wn.update()
                if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290: game_over = True
                if head.distance(food) < 20:
                    food.goto(random.randint(-280, 280), random.randint(-280, 280))
                    new_segment = turtle.Turtle(); new_segment.speed(0); new_segment.shape("square"); new_segment.color("lightgreen"); new_segment.penup()
                    segments.append(new_segment)
                    score += 10
                    if score > session_high_score: session_high_score = score
                    pen.clear(); pen.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))
                for i in range(len(segments)-1, 0, -1): segments[i].goto(segments[i-1].xcor(), segments[i-1].ycor())
                if len(segments) > 0: segments[0].goto(head.xcor(), head.ycor())
                move()
                for segment in segments:
                    if segment.distance(head) < 20: game_over = True
                time.sleep(delay)
            
            pen.goto(0,0); pen.write("GAME OVER", align="center", font=("Courier", 30, "normal"))
            wn.update()
            time.sleep(2)
            
            # Reset the game state for the next round
            head.goto(0,0)
            head.direction = "stop"
            for segment in segments:
                segment.goto(1000, 1000)
            segments.clear()
            score = 0
            pen.clear()
            pen.goto(0, 260)
            pen.write("Score: 0", align="center", font=("Courier", 24, "normal"))
    except (turtle.Terminator, tk.TclError):
        # When the user closes the window, return their highest score from the session
        return session_high_score
# ==============================================================================
# SECTION 3: ENHANCED TKINTER GUI (FRONTEND)
# ==============================================================================
# --- Style and Color Constants ---
BG_COLOR = "#2c3e50"
FRAME_COLOR = "#34495e"
TEXT_COLOR = "#ecf0f1"
PRIMARY_COLOR = "#1abc9c"
PRIMARY_HOVER_COLOR = "#16a085"
SECONDARY_COLOR = "#3498db"
SECONDARY_HOVER_COLOR = "#2980b9"
LARGE_FONT = ("Segoe UI", 18, "bold")
NORMAL_FONT = ("Segoe UI", 10)
BUTTON_FONT = ("Segoe UI", 12, "bold")
class GameApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Hub")
        self.geometry("600x450")
        self.configure(bg=BG_COLOR)
        self.current_user = None
        self.setup_styles()
        self.container = ttk.Frame(self, style="Main.TFrame")
        self.container.pack(side="top", fill="both", expand=True, padx=10, pady=10)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (LoginFrame, MainMenuFrame):
            frame = F(self.container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(LoginFrame)
    def setup_styles(self):
        """Configures the styles for all ttk widgets."""
        style = ttk.Style(self)
        style.theme_use('clam')
        # Configure frame styles
        style.configure('Main.TFrame', background=BG_COLOR)
        style.configure('Content.TFrame', background=FRAME_COLOR)
        # Configure label styles
        style.configure('Header.TLabel', background=FRAME_COLOR, foreground=TEXT_COLOR, font=LARGE_FONT)
        style.configure('TLabel', background=FRAME_COLOR, foreground=TEXT_COLOR, font=NORMAL_FONT)
        
        # Configure entry widget style
        style.configure('TEntry', fieldbackground="#2c3e50", foreground=TEXT_COLOR, insertcolor=TEXT_COLOR, borderwidth=2)
        style.map('TEntry', bordercolor=[('focus', PRIMARY_COLOR)])
        # Configure button styles
        style.configure('Primary.TButton', background=PRIMARY_COLOR, foreground="white", font=BUTTON_FONT, borderwidth=0)
        style.map('Primary.TButton', background=[('active', PRIMARY_HOVER_COLOR), ('!disabled', PRIMARY_COLOR)])
        
        style.configure('Secondary.TButton', background=SECONDARY_COLOR, foreground="white", font=BUTTON_FONT, borderwidth=0)
        style.map('Secondary.TButton', background=[('active', SECONDARY_HOVER_COLOR), ('!disabled', SECONDARY_COLOR)])
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
class LoginFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style='Content.TFrame')
        self.controller = controller
        ttk.Label(self, text="🎮 Game Hub Login", style='Header.TLabel').pack(pady=20)
        
        ttk.Label(self, text="Username").pack(pady=(10,0))
        self.username_entry = ttk.Entry(self, width=40, font=NORMAL_FONT)
        self.username_entry.pack(pady=5, padx=50)
        
        ttk.Label(self, text="Password").pack(pady=(10,0))
        self.password_entry = ttk.Entry(self, show="*", width=40, font=NORMAL_FONT)
        self.password_entry.pack(pady=5, padx=50)
        
        button_frame = ttk.Frame(self, style='Content.TFrame')
        button_frame.pack(pady=30)
        
        ttk.Button(button_frame, text="Login", style='Primary.TButton', command=self.attempt_login).grid(row=0, column=0, padx=10, ipady=5)
        ttk.Button(button_frame, text="Register", style='Secondary.TButton', command=self.attempt_register).grid(row=0, column=1, padx=10, ipady=5)
    def attempt_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if login_user(username, password):
            self.controller.current_user = username
            self.controller.frames[MainMenuFrame].update_welcome_message()
            self.controller.show_frame(MainMenuFrame)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")
    def attempt_register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        success, message = register_user(username, password)
        if success:
            messagebox.showinfo("Success", message)
        else:
            messagebox.showerror("Error", message)
class MainMenuFrame(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, style='Content.TFrame')
        self.controller = controller
        
        self.welcome_label = ttk.Label(self, text="", style='Header.TLabel')
        self.welcome_label.pack(pady=20)
        
        ttk.Button(self, text="🎲 Play Number Guessing", style='Primary.TButton', command=self.run_game1).pack(pady=5, ipady=8, padx=50, fill='x')
        ttk.Button(self, text="🗿 Play Rock, Paper, Scissors", style='Primary.TButton', command=self.run_game2).pack(pady=5, ipady=8, padx=50, fill='x')
        ttk.Button(self, text="🐍 Play Snake Game", style='Primary.TButton', command=self.run_game3).pack(pady=5, ipady=8, padx=50, fill='x')
        ttk.Button(self, text="🏆 Show My Scores", style='Secondary.TButton', command=self.show_my_scores).pack(pady=10, ipady=8, padx=50, fill='x')
        ttk.Button(self, text="Logout", command=self.logout).pack(pady=5, ipady=8, padx=50, fill='x')
    def update_welcome_message(self):
        self.welcome_label.config(text=f"Welcome, {self.controller.current_user}!")
    def run_game1(self):
        score = play_number_guessing_game()
        if score != "Cancelled":
            message = update_score(self.controller.current_user, 'game1_number_guess', score)
            messagebox.showinfo("Score Update", message)
    def run_game2(self):
        score = play_rps_game()
        if score != "Cancelled":
            message = update_score(self.controller.current_user, 'game2_rps', score)
            messagebox.showinfo("Score Update", message)
    def run_game3(self):
        score = play_snake_game()
        message = update_score(self.controller.current_user, 'game3_snake', score)
        messagebox.showinfo("Score Update", message)
    def show_my_scores(self):
        scores_text = get_player_scores_display(self.controller.current_user)
        messagebox.showinfo("Your Scores", scores_text)
    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame(LoginFrame)
if __name__ == "__main__":
    app = GameApp()
    app.mainloop()
