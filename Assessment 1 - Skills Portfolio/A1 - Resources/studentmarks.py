from tkinter import *
from tkinter import messagebox
import os

# ---------- load data ----------
def load_students():
    students = []
    path = r"C:\Users\Fathima hanna\Documents\GitHub\skills-portfolio-fathimahannah\Assessment 1 - Skills Portfolio\A1 - Resources\studentMarks.txt"
    try:
        with open(path) as f:
            lines = f.read().splitlines()
        for ln in lines[1:]:          # skip first line (count)
            if ln.strip():
                parts = ln.split(",")
                code  = parts[0].strip()
                name  = parts[1].strip()
                cw    = [int(parts[2]), int(parts[3]), int(parts[4])]
                exam  = int(parts[5])
                students.append({"code": code, "name": name, "cw": cw, "exam": exam})
    except FileNotFoundError:
        messagebox.showerror("Error", "studentMarks.txt not found.")
    return students

# ---------- calculate results ----------
def calc(s):
    total_cw = sum(s["cw"])           # out of 60
    total    = total_cw + s["exam"]   # out of 160
    pct      = (total / 160) * 100
    if   pct >= 70: grade = "A"
    elif pct >= 60: grade = "B"
    elif pct >= 50: grade = "C"
    elif pct >= 40: grade = "D"
    else:           grade = "F"
    return total_cw, pct, grade

# ---------- build a result card ----------
def make_card(parent, s, row):
    total_cw, pct, grade = calc(s)

    grade_colors = {"A": "#d5f5d5", "B": "#cce6ff", "C": "#fff9cc",
                    "D": "#ffe5cc", "F": "#ffd6e0"}
    color = grade_colors.get(grade, "#f0f0f0")

    card = Frame(parent, bg=color, bd=1, relief=SOLID, padx=12, pady=8)
    card.grid(row=row, column=0, sticky="ew", pady=5, padx=10)
    parent.columnconfigure(0, weight=1)

    Label(card, text=f"{s['name']}  ({s['code']})",
          font=("Arial", 13, "bold"), bg=color, anchor="w").pack(fill=X)

    info = (f"Coursework: {total_cw}/60    "
            f"Exam: {s['exam']}/100    "
            f"Percentage: {pct:.1f}%    "
            f"Grade: {grade}")
    Label(card, text=info, font=("Arial", 11), bg=color, anchor="w").pack(fill=X)

# ---------- screens ----------
def show_all():
    clear_content()
    Label(content, text="All Student Records",
          font=("Arial", 16, "bold"), bg="white").pack(pady=(10, 5))

    box = Frame(content, bg="white")
    box.pack(fill=BOTH, expand=True, padx=10)

    for i, s in enumerate(students):
        make_card(box, s, i)

    avg = sum(calc(s)[1] for s in students) / len(students)
    Label(content,
          text=f"Total students: {len(students)}    Average: {avg:.1f}%",
          font=("Arial", 12), bg="white", fg="#555").pack(pady=10)

def show_individual():
    clear_content()
    Label(content, text="View Individual Student",
          font=("Arial", 16, "bold"), bg="white").pack(pady=(10, 5))

    Label(content, text="Enter name or student code:",
          font=("Arial", 12), bg="white").pack()

    entry = Entry(content, font=("Arial", 12), width=25)
    entry.pack(pady=6)

    result_frame = Frame(content, bg="white")
    result_frame.pack(fill=X, padx=10)

    def search():
        for w in result_frame.winfo_children():
            w.destroy()
        q = entry.get().strip().lower()
        found = [s for s in students
                 if q == s["code"].lower() or q == s["name"].lower()]
        if found:
            make_card(result_frame, found[0], 0)
        else:
            Label(result_frame, text="No student found.",
                  font=("Arial", 12), bg="white", fg="red").grid(row=0)

    Button(content, text="Search", font=("Arial", 12),
           bg="#cce6ff", relief=FLAT, command=search).pack(pady=4)

def show_highest():
    clear_content()
    Label(content, text="Highest Overall Mark",
          font=("Arial", 16, "bold"), bg="white").pack(pady=(10, 5))
    best = max(students, key=lambda s: calc(s)[1])
    box = Frame(content, bg="white")
    box.pack(fill=X, padx=10)
    make_card(box, best, 0)

def show_lowest():
    clear_content()
    Label(content, text="Lowest Overall Mark",
          font=("Arial", 16, "bold"), bg="white").pack(pady=(10, 5))
    worst = min(students, key=lambda s: calc(s)[1])
    box = Frame(content, bg="white")
    box.pack(fill=X, padx=10)
    make_card(box, worst, 0)

# ---------- helpers ----------
def clear_content():
    for w in content.winfo_children():
        w.destroy()

# ---------- main window ----------
students = load_students()

root = Tk()
root.title("Student Manager")
root.geometry("750x580")
root.config(bg="white")

# top menu bar
menu_bar = Frame(root, bg="#e8f4fd", pady=8)
menu_bar.pack(fill=X)

btn_style = {"font": ("Arial", 12), "bg": "#cce6ff", "relief": FLAT,
             "padx": 14, "pady": 6, "cursor": "hand2",
             "activebackground": "#b3d9ff"}

Button(menu_bar, text="All Records",  command=show_all,        **btn_style).pack(side=LEFT, padx=6)
Button(menu_bar, text="Find Student", command=show_individual, **btn_style).pack(side=LEFT, padx=6)
Button(menu_bar, text="Highest Mark", command=show_highest,    **btn_style).pack(side=LEFT, padx=6)
Button(menu_bar, text="Lowest Mark",  command=show_lowest,     **btn_style).pack(side=LEFT, padx=6)

# scrollable content area
canvas = Canvas(root, bg="white", highlightthickness=0)
scrollbar = Scrollbar(root, orient=VERTICAL, command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side=RIGHT, fill=Y)
canvas.pack(side=LEFT, fill=BOTH, expand=True)

content = Frame(canvas, bg="white")
canvas.create_window((0, 0), window=content, anchor="nw")

def on_resize(e):
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.itemconfig(1, width=canvas.winfo_width())

content.bind("<Configure>", on_resize)

root.mainloop()