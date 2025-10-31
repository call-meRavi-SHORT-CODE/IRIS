import threading
import io
import sys
import time

# UI
try:
    import customtkinter as ctk
except Exception:  # fallback to tkinter if customtkinter is not installed
    import tkinter as ctk  # type: ignore
    from tkinter import scrolledtext  # type: ignore
else:
    from tkinter import scrolledtext  # ctk relies on tkinter widgets underneath
from tkinter import Canvas

# Speech (optional)
try:
    import speech_recognition as sr  # type: ignore
except Exception:  # voice will be disabled if not available
    sr = None  # type: ignore

from app import run_agent_collect


class IrisGUI:
    def __init__(self) -> None:
        if hasattr(ctk, "set_appearance_mode"):
            ctk.set_appearance_mode("dark")
        if hasattr(ctk, "set_default_color_theme"):
            ctk.set_default_color_theme("blue")

        self.root = ctk.CTk() if hasattr(ctk, "CTk") else ctk.Tk()
        self.root.title("IRIS - Voice/Text Controller")
        self.root.geometry("520x420")

        # Input row
        self.input_var = ctk.StringVar() if hasattr(ctk, "StringVar") else None
        self.entry = (ctk.CTkEntry(self.root, textvariable=self.input_var, placeholder_text="Type a command…")
                      if hasattr(ctk, "CTkEntry") else ctk.Entry(self.root))
        self.entry.pack(fill="x", padx=14, pady=(14, 8))

        buttons_frame = ctk.CTkFrame(self.root) if hasattr(ctk, "CTkFrame") else ctk.Frame(self.root)
        buttons_frame.pack(fill="x", padx=14)

        self.send_btn = (ctk.CTkButton(buttons_frame, text="Send", command=self.on_send)
                         if hasattr(ctk, "CTkButton") else ctk.Button(buttons_frame, text="Send", command=self.on_send))
        self.send_btn.pack(side="left", padx=(0, 8))

        mic_text = "Speak" if sr else "Speak (unavailable)"
        self.mic_btn = (ctk.CTkButton(buttons_frame, text=mic_text, command=self.on_speak, state=("normal" if sr else "disabled"))
                        if hasattr(ctk, "CTkButton") else ctk.Button(buttons_frame, text=mic_text, command=self.on_speak, state=("normal" if sr else "disabled")))
        self.mic_btn.pack(side="left")

        # Output (single-current message mode)
        self.output = scrolledtext.ScrolledText(self.root, height=12, wrap="word")
        self.output.pack(fill="both", expand=True, padx=14, pady=(10, 8))
        self.output.insert("end", "IRIS ready. Type a command or press Speak.\n")
        self.output.configure(state="disabled")

        # Mic animation canvas (hidden by default)
        self.anim_canvas = Canvas(self.root, height=58, highlightthickness=0)
        self.anim_canvas.configure(bg="#1a1a1a" if hasattr(ctk, "set_appearance_mode") else None)
        self.anim_visible = False
        self.animating = False
        self._anim_phase = 0.0

        self.entry.bind("<Return>", lambda _e: self.on_send())

    def set_output(self, text: str) -> None:
        """Replace history: only show the latest request/response."""
        self.output.configure(state="normal")
        self.output.delete("1.0", "end")
        self.output.insert("end", f"{text}\n")
        self.output.see("end")
        self.output.configure(state="disabled")

    def _show_animation(self) -> None:
        if self.anim_visible:
            return
        self.anim_canvas.pack(fill="x", padx=14, pady=(0, 12))
        self.anim_visible = True
        self.animating = True
        self._animate_tick()

    def _hide_animation(self) -> None:
        self.animating = False
        if self.anim_visible:
            # give a tiny delay to let the last frame settle
            self.root.after(150, lambda: (self.anim_canvas.pack_forget(), setattr(self, "anim_visible", False)))

    def _animate_tick(self) -> None:
        if not self.animating:
            return
        w = self.anim_canvas.winfo_width() or 480
        h = self.anim_canvas.winfo_height() or 58
        self.anim_canvas.delete("all")
        self._anim_phase = (self._anim_phase + 0.12) % 6.283  # 2π cycle
        center_y = h // 2
        bar_count = 18
        spacing = w / (bar_count + 2)
        max_bar = h * 0.38
        for i in range(bar_count):
            x = (i + 1) * spacing
            # Offset each bar with a phase shift to create a wave
            amp = (max_bar * 0.25) + (max_bar * 0.75) * (0.5 + 0.5 * __import__("math").sin(self._anim_phase + i * 0.35))
            self.anim_canvas.create_line(x, center_y - amp, x, center_y + amp, width=4, fill="#3aa3ff")
        self.root.after(50, self._animate_tick)

    def on_send(self) -> None:
        text = self.entry.get() if hasattr(self.entry, "get") else (self.input_var.get() if self.input_var else "")
        if not text.strip():
            return
        self.entry.delete(0, "end")
        self.set_output(f"You: {text}")
        threading.Thread(target=self._run_agent, args=(text,), daemon=True).start()

    def _run_agent(self, prompt: str) -> None:
        try:
            result_text = run_agent_collect(prompt)
        except Exception as e:
            result_text = f"Error: {e}"
        self.set_output(result_text or "(no response)")

    def on_speak(self) -> None:
        if not sr:
            return
        self.set_output("Listening…")
        # Disable buttons during capture and show animation
        self.send_btn.configure(state="disabled")
        self.mic_btn.configure(state="disabled")
        self._show_animation()
        threading.Thread(target=self._transcribe_and_send, daemon=True).start()

    def _transcribe_and_send(self) -> None:
        assert sr is not None
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            text = recognizer.recognize_google(audio)
        except Exception as e:
            self._hide_animation()
            self.send_btn.configure(state="normal")
            self.mic_btn.configure(state="normal")
            self.set_output(f"Voice error: {e}")
            return
        self.set_output(f"You (voice): {text}")
        self._hide_animation()
        self.send_btn.configure(state="normal")
        self.mic_btn.configure(state="normal")
        self._run_agent(text)

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    IrisGUI().run()


