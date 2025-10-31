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

# Speech (optional)
try:
    import speech_recognition as sr  # type: ignore
except Exception:  # voice will be disabled if not available
    sr = None  # type: ignore

from app import run_agent_collect


class IrisGUI:
    def __init__(self) -> None:
        # Configure appearance for CustomTkinter; harmless for std tkinter
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

        # Output
        self.output = scrolledtext.ScrolledText(self.root, height=16, wrap="word")
        self.output.pack(fill="both", expand=True, padx=14, pady=14)
        self.output.insert("end", "IRIS ready. Type a command or press Speak.\n")
        self.output.configure(state="disabled")

        self.entry.bind("<Return>", lambda _e: self.on_send())

    def append_output(self, text: str) -> None:
        self.output.configure(state="normal")
        self.output.insert("end", f"{text}\n")
        self.output.see("end")
        self.output.configure(state="disabled")

    def on_send(self) -> None:
        text = self.entry.get() if hasattr(self.entry, "get") else (self.input_var.get() if self.input_var else "")
        if not text.strip():
            return
        self.entry.delete(0, "end")
        self.append_output(f"You: {text}")
        threading.Thread(target=self._run_agent, args=(text,), daemon=True).start()

    def _run_agent(self, prompt: str) -> None:
        try:
            result_text = run_agent_collect(prompt)
        except Exception as e:
            result_text = f"Error: {e}"
        self.append_output(result_text or "(no response)")

    def on_speak(self) -> None:
        if not sr:
            return
        self.append_output("Listening…")
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
            self.append_output(f"Voice error: {e}")
            return
        self.append_output(f"You (voice): {text}")
        self._run_agent(text)

    def run(self) -> None:
        self.root.mainloop()


if __name__ == "__main__":
    IrisGUI().run()


