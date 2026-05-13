from tkinter import *
from tkinter import messagebox
import random
import os
from PIL import Image, ImageTk 

# create a new math question based on chosen difficulty
def generate_question():
    global right_answer, question_number, score, difficulty
    
    if difficulty == "Easy":
        limit, ops = 10, ["+", "-"]
    elif difficulty == "Moderate":
        limit, ops = 20, ["*", "//"]
    else:
        limit, ops = 60, ["+", "-", "*", "//"]

    a, b = random.randint(1, limit), random.randint(1, limit)
    op = random.choice(ops)

    if op == "//" and b == 0:
        b = 1

    question_label.config(text=f"What is {a} {op} {b}?")
    right_answer = eval(f"{a}{op}{b}")

# check user's answer and move to next question
def submit_answer():
    global score, question_number
    try:
        ans = int(answer_box.get())
    except ValueError:
        messagebox.showwarning("Error", "Enter a number.")
        return

    if ans == right_answer:
        score += 1

    answer_box.delete(0, END)

    if question_number < 5:
        question_number += 1
        generate_question()
    else:
        show_results()

# start the quiz after picking difficulty 
def start_quiz(level):
    global score, question_number, difficulty
    difficulty = level
    score = 0
    question_number = 1
    show_frame(frame_quiz)
    generate_question()

# display the final score screen at the end of the quiz
def show_results():
    show_frame(frame_score)
    result_label.config(text=f"Your Score: {score} / 5")

# return back to the home screen
def go_home():
    show_frame(frame_start)

# open the difficulty selection screen
def pick_difficulty():
    show_frame(frame_difficulty)

# ask the user if they want to close the app
def confirm_exit():
    if messagebox.askyesno("Exit", "Close the app?"):
        root.destroy()

# set a background image that automatically resizes with the window
def make_background_dynamic(frame, img_path):
    bg_img = Image.open(img_path)
    bg_label = Label(frame)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    # update background size when window is resized
    def resize_bg(event):
        img_resized = bg_img.resize((event.width, event.height))
        bg_photo = ImageTk.PhotoImage(img_resized)
        bg_label.config(image=bg_photo)
        bg_label.image = bg_photo

    frame.bind("<Configure>", resize_bg)

# hide all frames and show only the selected one
def show_frame(frame):
    for f in all_frames:
        f.pack_forget()
    frame.pack(fill="both", expand=True)

root = Tk()
root.title("Math Quiz")
root.geometry("900x650")
root.protocol("WM_DELETE_WINDOW", confirm_exit)

IMG_PATH = os.path.join(os.path.dirname(__file__), "1.jpg")

frame_start = Frame(root)
frame_difficulty = Frame(root)
frame_quiz = Frame(root)
frame_score = Frame(root)

all_frames = [frame_start, frame_difficulty, frame_quiz, frame_score]

for f in all_frames:
    make_background_dynamic(f, IMG_PATH)

Label(frame_start, text="Welcome to the Math Quiz!", font=("Arial", 28), bg="white").pack(pady=150)
Button(frame_start, text="Start Quiz", font=("Arial", 18), bg="#cce6ff",
       activebackground="#b3d9ff", command=pick_difficulty).pack()

Label(frame_difficulty, text="Choose Difficulty", font=("Arial", 24), bg="white").pack(pady=80)
Button(frame_difficulty, text="Easy", font=("Arial", 16), width=20, bg="#d5f5d5",
       activebackground="#c4efc4", command=lambda: start_quiz("Easy")).pack(pady=10)
Button(frame_difficulty, text="Medium", font=("Arial", 16), width=20, bg="#fff9cc",
       activebackground="#fff2a3", command=lambda: start_quiz("Moderate")).pack(pady=10)
Button(frame_difficulty, text="Hard", font=("Arial", 16), width=20, bg="#ffd6e0",
       activebackground="#ffbfd0", command=lambda: start_quiz("Hard")).pack(pady=10)

question_label = Label(frame_quiz, text="", font=("Arial", 22), bg="white")
question_label.pack(pady=80)

answer_box = Entry(frame_quiz, font=("Arial", 18), width=10)
answer_box.pack()

Button(frame_quiz, text="Submit", font=("Arial", 16), bg="#cce6ff",
       activebackground="#b3d9ff", command=submit_answer).pack(pady=20)

result_label = Label(frame_score, text="", font=("Arial", 26), bg="white")
result_label.pack(pady=120)

Button(frame_score, text="Home", font=("Arial", 16), bg="#d5f5d5",
       activebackground="#c4efc4", command=go_home).pack()

show_frame(frame_start)
root.mainloop()