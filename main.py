import customtkinter as ctk
import pyautogui
import time
import threading
import sys

# Configure appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class TextRepeaterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Unlimited Text Sender (Rate Limited)")
        self.geometry("450x550")
        self.resizable(False, False)

        self.is_running = False

        # --- UI Elements ---
        
        # Title Label
        self.title_label = ctk.CTkLabel(self, text="Text Sender Pro", font=("Helvetica", 24, "bold"))
        self.title_label.pack(pady=(20, 10))

        # Instructions Label
        self.instruction_label = ctk.CTkLabel(self, text="Keep your mouse near a corner\nto Emergency Stop if needed!", text_color="#ff5555", font=("Helvetica", 13))
        self.instruction_label.pack(pady=(0, 20))

        # Text input
        self.text_label = ctk.CTkLabel(self, text="Message to send:")
        self.text_label.pack(anchor="w", padx=40)
        self.text_input = ctk.CTkTextbox(self, height=100)
        self.text_input.pack(fill="x", padx=40, pady=(0, 20))

        # Count slider
        self.count_label = ctk.CTkLabel(self, text="Number of messages: 10")
        self.count_label.pack(anchor="w", padx=40)
        self.count_slider = ctk.CTkSlider(self, from_=1, to=1000, command=self.update_count_label)
        self.count_slider.set(10)
        self.count_slider.pack(fill="x", padx=40, pady=(0, 20))

        # Rate Limit slider (Delay)
        self.delay_label = ctk.CTkLabel(self, text="Rate Limit Delay: 1.0 seconds")
        self.delay_label.pack(anchor="w", padx=40)
        self.delay_slider = ctk.CTkSlider(self, from_=0.1, to=5.0, command=self.update_delay_label)
        self.delay_slider.set(1.0)
        self.delay_slider.pack(fill="x", padx=40, pady=(0, 20))

        # Status Label
        self.status_label = ctk.CTkLabel(self, text="Status: Ready", text_color="#55ff55")
        self.status_label.pack(pady=10)

        # Action Buttons
        self.start_btn = ctk.CTkButton(self, text="START (5s Prep Delay)", fg_color="#28a745", hover_color="#218838", command=self.start_sending)
        self.start_btn.pack(pady=(10, 5), padx=40, fill="x")

        self.stop_btn = ctk.CTkButton(self, text="STOP", fg_color="#dc3545", hover_color="#c82333", command=self.stop_sending, state="disabled")
        self.stop_btn.pack(pady=5, padx=40, fill="x")


    def update_count_label(self, value):
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

        self.is_running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        
        # Start in a new thread to keep UI responsive
        threading.Thread(target=self.sending_task, args=(text, count, delay), daemon=True).start()

    def stop_sending(self):
        self.is_running = False
        self.status_label.configure(text="Status: Stopped by user", text_color="#ff5555")
        self.reset_buttons()

    def reset_buttons(self):
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")

    def sending_task(self, text, count, delay):
        try:
            # 5 seconds grace period
            for i in range(5, 0, -1):
                if not self.is_running: return
                self.status_label.configure(text=f"Starting in {i} seconds... Click your chat!", text_color="#ffaa00")
                time.sleep(1)

            for i in range(count):
                if not self.is_running:
                    break
                
                self.status_label.configure(text=f"Sending {i+1} of {count}...", text_color="#55ffff")
                
                # Type the message and press enter
                # Adding a tiny interval between keystrokes to act like a real person typing
                pyautogui.write(text, interval=0.005)
                pyautogui.press("enter")
                
                # Rate limit delay (sleep)
                time.sleep(delay)

            if self.is_running:
                self.status_label.configure(text="Status: Finished!", text_color="#55ff55")
                self.is_running = False
        
        except pyautogui.FailSafeException:
            # If user mouse matches screen corner
            self.is_running = False
            self.status_label.configure(text="Status: Emergency Fail-Safe triggered!", text_color="#ff5555")
        
        except Exception as e:
            self.is_running = False
            self.status_label.configure(text=f"Error: {str(e)}", text_color="#ff5555")

        self.reset_buttons()

if __name__ == "__main__":
    app = TextRepeaterApp()
    app.mainloop()
