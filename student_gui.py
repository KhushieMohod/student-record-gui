import tkinter as tk
from tkinter import messagebox, filedialog

students = []

# ------------------------ Core Logic -----------------------------

def add_student():
    name = name_entry.get()
    roll = roll_entry.get()
    sgpa = sgpa_entry.get()

    if not name or not roll or not sgpa:
        messagebox.showwarning("Input Error", "Please fill all fields.")
        return

    try:
        sgpa = float(sgpa)
        if not (0.0 <= sgpa <= 10.0):
            raise ValueError
    except ValueError:
        messagebox.showerror("Input Error", "SGPA must be a number between 0 and 10.")
        return

    students.append({"name": name, "roll": roll, "sgpa": sgpa})
    messagebox.showinfo("Success", "Student added successfully!")
    clear_entries()

def clear_entries():
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    sgpa_entry.delete(0, tk.END)

def view_students():
    text_area.delete("1.0", tk.END)
    if not students:
        text_area.insert(tk.END, "No student records available.\n")
    else:
        for i, student in enumerate(students, 1):
            text_area.insert(tk.END, f"{i}. Name: {student['name']}, Roll: {student['roll']}, SGPA: {student['sgpa']}\n")

def save_to_file():
    with open("students.txt", "w") as f:
        for student in students:
            f.write(f"{student['name']},{student['roll']},{student['sgpa']}\n")
    messagebox.showinfo("Saved", "Records saved to students.txt")

def load_from_file():
    try:
        with open("students.txt", "r") as f:
            students.clear()
            for line in f:
                name, roll, sgpa = line.strip().split(",")
                students.append({"name": name, "roll": roll, "sgpa": float(sgpa)})
        messagebox.showinfo("Loaded", "Records loaded from students.txt")
        view_students()
    except FileNotFoundError:
        messagebox.showerror("Error", "students.txt file not found.")
    except:
        messagebox.showerror("Error", "Error reading file.")

def calculate_cgpa():
    if not students:
        messagebox.showwarning("No Data", "No students to calculate CGPA.")
        return
    total = sum(student['sgpa'] for student in students)
    cgpa = total / len(students)
    messagebox.showinfo("CGPA", f"Average CGPA of all students: {cgpa:.2f}")

def exit_app():
    root.quit()

# ------------------------ GUI Layout -----------------------------

root = tk.Tk()
root.title("Student Record System")
root.geometry("500x500")

# Input Labels and Fields
tk.Label(root, text="Name").grid(row=0, column=0, padx=10, pady=5, sticky="e")
tk.Label(root, text="Roll No").grid(row=1, column=0, padx=10, pady=5, sticky="e")
tk.Label(root, text="SGPA").grid(row=2, column=0, padx=10, pady=5, sticky="e")

name_entry = tk.Entry(root, width=30)
roll_entry = tk.Entry(root, width=30)
sgpa_entry = tk.Entry(root, width=30)

name_entry.grid(row=0, column=1, pady=5)
roll_entry.grid(row=1, column=1, pady=5)
sgpa_entry.grid(row=2, column=1, pady=5)

# Buttons
tk.Button(root, text="Add Student", command=add_student).grid(row=3, column=1, pady=10, sticky="w")
tk.Button(root, text="View Students", command=view_students).grid(row=3, column=1, pady=10, sticky="e")
tk.Button(root, text="Calculate CGPA", command=calculate_cgpa).grid(row=4, column=1, pady=5)

# Text Display
text_area = tk.Text(root, height=10, width=60)
text_area.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

# Menu Bar
menu_bar = tk.Menu(root)
file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Save", command=save_to_file)
file_menu.add_command(label="Load", command=load_from_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app)

menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar)

root.mainloop()
