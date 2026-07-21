# gamblinginator3000 v3
import tkinter as tk
import random

# catpuccin colours :3
BASE = "#1e1e2e"
TEXT = "#cdd6f4"
MAUVE = "#cba6f7"
YELLOW = "#f9e2af" 
SAPHIRE = "#74c7ec"

# animation of spinning :3
SPIN_FRAMES = ["-", "\\", "|", "/"]

def animate(frame_index, remaining_steps):
    if remaining_steps > 0:
        # show spinning coin frames
        lbl.config(text=SPIN_FRAMES[frame_index % 4], fg=TEXT)
        # call this function again in 50 ms
        root.after(50, animate, frame_index + 1, remaining_steps - 1)
    else:
        # animation done, pick result
        result = random.choice(["Heads :3", "Tails :3"])
        color = YELLOW if result == "Heads :3" else SAPHIRE
        lbl.config(text=result, fg=color)
        btn.config(state="normal")

def start_flip():
    btn.config(state="disabled") # to prevent double clicks
    animate(0, 15) # 0 is starting frame and 15 is total number of flips

root = tk.Tk()
root.title("gamblinginator3000")
root.geometry("140x90")
root.configure(bg=BASE)
root.resizable(False, False)


lbl = tk.Label(root, text="?", font=("Arial", 14, "bold"), bg=BASE, fg=TEXT)
lbl.pack(pady=8)

btn = tk.Button(root, text="Flip", font=("Arial", 9, "bold"), bg="#313244", fg=MAUVE, activebackground=MAUVE, activeforeground=BASE, bd=0, command=start_flip)
btn.pack(fill="x", padx=20)

root.mainloop()
