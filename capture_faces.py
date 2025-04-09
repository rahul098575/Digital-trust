def capture_faces():
    # Step 1: Get name input on main thread
    name = simpledialog.askstring("Capture Face", "Enter the person's name:", parent=root)
    if not name:
        messagebox.showwarning("Input Error", "Name cannot be empty.")
        return

    # Step 2: Run face capture subprocess in background thread
    def run_capture():
        try:
            subprocess.run(["python", "capture_faces.py", name], check=True)
            root.after(0, lambda: messagebox.showinfo("Success", f"Face data captured for {name}"))
        except subprocess.CalledProcessError as e:
            root.after(0, lambda: messagebox.showerror("Capture Failed", f"Error:\n{e}"))
        finally:
            progress.stop()
            progress.lower()

    progress.lift()
    progress.start()
    threading.Thread(target=run_capture).start()
