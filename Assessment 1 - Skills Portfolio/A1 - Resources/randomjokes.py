from tkinter import *
from tkinter import messagebox
import random
from PIL import Image, ImageTk

# Load jokes from a text file and store as (question, answer) tuples
def fetch_jokes():
    path = r"C:\Users\user\Documents\GitHub\skills-portfolio-fathimahannah\Assessment 1 - Skills Portfolio\A1 - Resources\randomJokes.txt"
    out = []
    try:
        with open(path) as f:
            for ln in f:
                if "?" in ln:
                    q, a = ln.split("?", 1)
                    out.append((q.strip() + "?", a.strip()))
    except FileNotFoundError:
        messagebox.showerror("Missing File", "Cannot locate randomJokes.txt")
    return out

# Set a frame background dynamically and resize with window
def apply_bg(frame, img_path):
    img_orig = Image.open(img_path)
    lbl = Label(frame)
    lbl.place(x=0, y=0, relwidth=1, relheight=1)
    def resize(event):
        img_resized = img_orig.resize((event.width, event.height))
        photo = ImageTk.PhotoImage(img_resized)
        lbl.config(image=photo)
        lbl.image = photo

    frame.bind("<Configure>", resize)


# Pick a new random joke and display question
def new_joke():
    global current
    if not joke_data:
        question_lbl.config(text="(No jokes available)")
        answer_lbl.config(text="")
        return
    current = random.choice(joke_data)
    question_lbl.config(text=current[0])
    answer_lbl.config(text="")
    reveal_btn.config(state=NORMAL)
    quit_btn.pack_forget() 

# Reveal the answer/punchline of the current joke
def show_answer():
    answer_lbl.config(text=current[1])
    reveal_btn.config(state=DISABLED)
    quit_btn.pack(pady=15)  

# Confirm exit before closing app
def leave():
    if messagebox.askyesno("Quit", "Exit the program?"):
        root.destroy()

# Switch from welcome screen to joke screen
def switch():
    screen1.pack_forget()
    screen2.pack(fill=BOTH, expand=True)

root = Tk()
root.title("Joke Machine")
root.geometry("800x600")
root.protocol("WM_DELETE_WINDOW", leave)

joke_data = fetch_jokes()  # Load jokes at start
current = None 

# Welcome screen with background
screen1 = Frame(root)
apply_bg(screen1, r"C:\Users\user\Documents\GitHub\skills-portfolio-fathimahannah\Assessment 1 - Skills Portfolio\A1 - Resources\2.jpg")
screen1.pack(expand=True, fill=BOTH)

Label(screen1, text="Welcome!", font=("Arial", 32), bg="white").pack(pady=170)
Button(screen1, text="Start", font=("Arial", 20), bg="#cce6ff", command=switch).pack()

# Joke screen with dynamic background
screen2 = Frame(root)
apply_bg(screen2, r"C:\Users\user\Documents\GitHub\skills-portfolio-fathimahannah\Assessment 1 - Skills Portfolio\A1 - Resources\2.jpg")

question_lbl = Label(screen2, text="", font=("Arial", 24), wraplength=650, justify=CENTER)
question_lbl.pack(pady=70)

answer_lbl = Label(screen2, text="", font=("Arial", 20), fg="grey", wraplength=650, justify=CENTER)
answer_lbl.pack()

Button(screen2, text="Joke", font=("Arial", 18), bg="#d5f5d5", command=new_joke).pack(pady=20)

reveal_btn = Button(screen2, text="Reveal Punchline", font=("Arial", 18), bg="#fff9cc", state=DISABLED, command=show_answer)
reveal_btn.pack()

quit_btn = Button(screen2, text="Exit", font=("Arial", 18), bg="#ffd6e0", command=leave)

root.mainloop()
