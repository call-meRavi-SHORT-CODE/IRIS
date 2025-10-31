import customtkinter as ctk
import tkinter as tk
import math
import threading
import time

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class SiriUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # === Frameless Window ===
        self.overrideredirect(True)
        self.geometry("400x150+600+300")
        self.configure(fg_color="#1E1E1E")

        # === Dragging variables ===
        self._offset_x = 0
        self._offset_y = 0

        # === Bind mouse events for dragging ===
        self.bind("<Button-1>", self.click_win)
        self.bind("<B1-Motion>", self.drag_win)

        # === Close Button ===
        self.close_btn = ctk.CTkButton(
            self, text="✕", width=25, height=25,
            corner_radius=5, fg_color="#2C2C2C", hover_color="#FF3B30",
            command=self.destroy
        )
        self.close_btn.place(x=365, y=10)

        # === Label ===
        self.label = ctk.CTkLabel(
            self, text="What can I help you with?",
            font=("Helvetica", 16, "bold"), text_color="white"
        )
        self.label.pack(pady=(40, 10))

        # === Canvas for Wave Animation ===
        self.canvas = tk.Canvas(self, bg="#1E1E1E", height=40, width=400, highlightthickness=0)
        self.canvas.pack()

        # === Ask Button ===
        self.ask_btn = ctk.CTkButton(
            self, text="Ask", width=100, command=self.start_listening,
            fg_color="#007AFF", hover_color="#005BBB"
        )
        self.ask_btn.pack(pady=10)

        # === Animation control ===
        self.animating = False

    # === Functions to move window ===
    def click_win(self, event):
        self._offset_x = event.x
        self._offset_y = event.y

    def drag_win(self, event):
        x = self.winfo_pointerx() - self._offset_x
        y = self.winfo_pointery() - self._offset_y
        self.geometry(f"+{x}+{y}")

    # === Listening animation ===
    def start_listening(self):
        if not self.animating:
            self.animating = True
            self.ask_btn.configure(text="Listening…", state="disabled")
            threading.Thread(target=self.animate_wave, daemon=True).start()

    def animate_wave(self):
        colors = ["#00AEEF", "#00FF9C", "#FF2D55"]
        t = 0
        while self.animating:
            self.canvas.delete("all")
            for i, color in enumerate(colors):
                points = []
                for x in range(0, 400, 5):
                    y = 20 + math.sin((x / 40) + t + i) * 10
                    points.append((x, y))
                for j in range(len(points) - 1):
                    self.canvas.create_line(points[j], points[j+1], fill=color, width=2, smooth=True)
            self.update_idletasks()
            t += 0.2
            time.sleep(0.03)
        self.canvas.delete("all")

    def stop_listening(self):
        self.animating = False
        self.ask_btn.configure(text="Ask", state="normal")

if __name__ == "__main__":
    app = SiriUI()
    app.mainloop()
