import customtkinter as ctk
import pyautogui
import time
import threading
import random

# Configure appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class TextRepeaterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Unlimited Text Sender (Pro)")
        self.geometry("450x650")
        self.resizable(False, False)
        
        # Always on top by default
        self.attributes("-topmost", True)
        self.is_running = False

        # --- UI Elements ---
        self.title_label = ctk.CTkLabel(self, text="Text Sender Pro", font=("Helvetica", 24, "bold"))
        self.title_label.pack(pady=(15, 5))

        self.instruction_label = ctk.CTkLabel(self, text="KEEP MOUSE NEAR A CORNER\nto Emergency Stop at any time!", text_color="#ff5555", font=("Helvetica", 13, "bold"))
        self.instruction_label.pack(pady=(0, 15))

        # Text input
        self.text_label = ctk.CTkLabel(self, text="Message to send:")
        self.text_label.pack(anchor="w", padx=40)
        self.text_input = ctk.CTkTextbox(self, height=80)
        self.text_input.pack(fill="x", padx=40, pady=(0, 15))

        # Options Frame
        self.options_frame = ctk.CTkFrame(self)
        self.options_frame.pack(fill="x", padx=40, pady=(0, 15))

        self.always_on_top_var = ctk.BooleanVar(value=True)
        self.top_switch = ctk.CTkSwitch(self.options_frame, text="Keep Window Always on Top", variable=self.always_on_top_var, command=self.toggle_topmost)
        self.top_switch.pack(pady=10, padx=10, anchor="w")

        self.infinite_var = ctk.BooleanVar(value=False)
        self.infinite_switch = ctk.CTkSwitch(self.options_frame, text="Infinite Mode (Send Until Stopped)", variable=self.infinite_var, command=self.toggle_infinite_mode)
        self.infinite_switch.pack(pady=(0, 10), padx=10, anchor="w")

        # Count slider
        self.count_label = ctk.CTkLabel(self, text="Number of messages: 20")
        self.count_label.pack(anchor="w", padx=40)
        self.count_slider = ctk.CTkSlider(self, from_=1, to=1000, command=self.update_count_label)
        self.count_slider.set(20)
        self.count_slider.pack(fill="x", padx=40, pady=(0, 15))

        # Rate Limit slider (Delay)
        self.delay_label = ctk.CTkLabel(self, text="Rate Limit Delay: 1.0 seconds\n(Protects from bans!)")
        self.delay_label.pack(anchor="w", padx=40)
        self.delay_slider = ctk.CTkSlider(self, from_=0.1, to=5.0, command=self.update_delay_label)
        self.delay_slider.set(1.0)
        self.delay_slider.pack(fill="x", padx=40, pady=(0, 15))

        # Status Label
        self.status_label = ctk.CTkLabel(self, text="Ready to send!", text_color="#55ff55")
        self.status_label.pack(pady=5)

        # Action Buttons
        self.start_btn = ctk.CTkButton(self, text="START (5s Prep Delay)", fg_color="#28a745", hover_color="#218838", font=("Helvetica", 14, "bold"), command=self.start_sending)
        self.start_btn.pack(pady=(5, 5), padx=40, fill="x", height=40)

        self.stop_btn = ctk.CTkButton(self, text="EMERGENCY STOP", fg_color="#dc3545", hover_color="#c82333", font=("Helvetica", 14, "bold"), command=self.stop_sending, state="disabled")
        self.stop_btn.pack(pady=5, padx=40, fill="x", height=40)


    def toggle_topmost(self):
        self.attributes("-topmost", self.always_on_top_var.get())

    def toggle_infinite_mode(self):
        if self.infinite_var.get():
            self.count_slider.configure(state="disabled")
            self.count_label.configure(text="Number of messages: INFINITE")
        else:
            self.count_slider.configure(state="normal")
            self.update_count_label(self.count_slider.get())

    def update_count_label(self, value):
        if not self.infinite_var.get():
            self.count_label.configure(text=f"Number of messages: {int(value)}")

    def update_delay_label(self, value):
        self.delay_label.configure(text=f"Rate Limit Delay: {value:.1f} seconds")

    def start_sending(self):
        text = self.text_input.get("1.0", "end-1c").strip()
        if not text:
            self.status_label.configure(text="Error: Message cannot be empty", text_color="#ff5555")
            return

        count = int(self.count_slider.get())
        delay = self.delay_slider.get()
        infinite = self.infinite_var.get()

        self.is_running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.text_input.configure(state="disabled")
        
        threading.Thread(target=self.sending_task, args=(text, count, delay, infinite), daemon=True).start()

    def stop_sending(self):
        self.is_running = False
        self.status_label.configure(text="Status: Stopped by user", text_color="#dc3545")
        self.reset_buttons()

    def reset_buttons(self):
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.text_input.configure(state="normal")

    def sending_task(self, text, count, delay, infinite):
        try:
            # 5 seconds grace period
            for i in range(5, 0, -1):
                if not self.is_running: return
                self.status_label.configure(text=f"Starting in {i}s... Click your chat!", text_color="#ffaa00")
                time.sleep(1)

            i = 0
            while self.is_running and (infinite or i < count):
                i += 1
                total_str = "∞" if infinite else str(count)
                self.status_label.configure(text=f"Sending {i} / {total_str}...", text_color="#55ffff")
                
                # Tiny random variation to mimic human typing
                type_speed = max(0.001, random.uniform(0.002, 0.015))
                pyautogui.write(text, interval=type_speed)
                pyautogui.press("enter")
                
                # Small random variation to the delay too
                actual_delay = delay + random.uniform(0.0, 0.3)
                time.sleep(actual_delay)

            if self.is_running:
                self.status_label.configure(text="Status: Finished!", text_color="#55ff55")
                self.is_running = False
        
        except pyautogui.FailSafeException:
            self.is_running = False
            self.status_label.configure(text="Emergency Fail-Safe triggered!", text_color="#dc3545")
        
        except Exception as e:
            self.is_running = False
            self.status_label.configure(text=f"Error: {str(e)}", text_color="#ff5555")

        self.reset_buttons()

if __name__ == "__main__":
    app = TextRepeaterApp()
    app.mainloop()
