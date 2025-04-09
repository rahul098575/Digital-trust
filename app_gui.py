import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import ttk
import subprocess
import threading
import os

# --- Main window setup ---
root = tk.Tk()
root.title("Face Recognition Attendance System")
root.geometry("500x400")
root.configure(bg="#f0f8ff")

# --- Title ---
tk.Label(root, text="Face Recognition Attendance System", font=("Segoe UI", 16, "bold"),
         bg="#f0f8ff", fg="#003366").pack(pady=20)

# --- Spinner ---
progress = ttk.Progressbar(root, mode="indeterminate", length=200)
progress.place(relx=0.5, rely=0.95, anchor="center")
progress.lower()

# --- Reusable styling function for buttons ---
def styled_button(master, text, command, bg_color):
    btn = tk.Button(master, text=text, font=("Segoe UI", 12), width=25, height=2,
                    bg=bg_color, fg="white", activebackground="#555", bd=0,
                    cursor="hand2", command=command)
    btn.pack(pady=15)
    return btn

# --- Capture Faces ---
def capture_faces():
    name = simpledialog.askstring("Capture Face", "Enter the person's name:", parent=root)
    if not name:
        messagebox.showwarning("Input Error", "Name cannot be empty.")
        return

    def run_capture():
        try:
            subprocess.run(["python", "capture_faces.py", name], check=True)
            messagebox.showinfo("Success", f"Face data captured for {name}")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Capture Failed", f"Error:\n{e}")
        finally:
            progress.stop()
            progress.lower()

    progress.lift()
    progress.start()
    threading.Thread(target=run_capture).start()

# --- Train Model ---
def train_model():
    def run_training():
        try:
            subprocess.run(["python", "train_model.py"], check=True)
            messagebox.showinfo("Success", "Model training completed.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Training Failed", f"Error:\n{e}")
        finally:
            progress.stop()
            progress.lower()

    progress.lift()
    progress.start()
    threading.Thread(target=run_training).start()

# --- Recognize and Export ---
def recognize_and_export():
    def run_export():
        try:
            subprocess.run(
                ["python", "export_summary.py"],
                check=True,
                cwd=os.getcwd()
            )
            messagebox.showinfo("Success", "Attendance marked and Excel exported.")
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Export Failed", f"Error:\n{e}")
        finally:
            progress.stop()
            progress.lower()

    progress.lift()
    progress.start()
    threading.Thread(target=run_export).start()

# --- Add buttons to the window ---
styled_button(root, "Capture Face", capture_faces, "#1e90ff")
styled_button(root, "Train Model", train_model, "#28a745")
styled_button(root, "Recognize & Export", recognize_and_export, "#ff8c00")

# --- Run the GUI ---
root.mainloop()
