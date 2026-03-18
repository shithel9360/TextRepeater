import customtkinter as ctk
import pyautogui
import time
import threading
import random
import pyperclip
import sys

# Configure appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class TextRepeaterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Unlimited Text Sender Pro")
        self.geometry("480x880")
        self.resizable(False, False)
        
        # Always on top by default
        self.attributes("-topmost", True)
        self.is_running = False

        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="⚡ Text Sender Pro", font=("Helvetica", 28, "bold"), text_color="#1f6aa5")
        self.title_label.pack(anchor="center")
        
        self.subtitle_label = ctk.CTkLabel(self.header_frame, text="Automated & Untraceable Messaging", font=("Helvetica", 12), text_color="gray")
        self.subtitle_label.pack(anchor="center")

        # --- Message Card ---
        self.msg_frame = ctk.CTkFrame(self)
        self.msg_frame.pack(fill="x", padx=20, pady=(10, 10))

        self.text_label = ctk.CTkLabel(self.msg_frame, text="📝 Message Payload", font=("Helvetica", 14, "bold"))
        self.text_label.pack(anchor="w", padx=15, pady=(10, 5))
        
        self.hint_label = ctk.CTkLabel(self.msg_frame, text="Tip: Use {count} to inject message numbers and bypass spam filters.", font=("Helvetica", 11), text_color="gray")
        self.hint_label.pack(anchor="w", padx=15, pady=(0, 5))

        self.text_input = ctk.CTkTextbox(self.msg_frame, height=100, border_width=1, border_color="#333333")
        self.text_input.pack(fill="x", padx=15, pady=(0, 5))

        self.nav_label = ctk.CTkLabel(self.msg_frame, text="🔀 Next Chat Key (Optional):", font=("Helvetica", 12, "bold"))
        self.nav_label.pack(anchor="w", padx=15, pady=(5, 0))
        
        self.nav_hint = ctk.CTkLabel(self.msg_frame, text="Type 'tab' to switch box, or 'ctrl+tab' / 'cmd+tab' for browser tabs!", font=("Helvetica", 11), text_color="gray")
        self.nav_hint.pack(anchor="w", padx=15, pady=0)

        self.nav_input = ctk.CTkEntry(self.msg_frame, placeholder_text="e.g. tab, down, ctrl+tab")
        self.nav_input.pack(fill="x", padx=15, pady=(5, 15))


        # --- Settings Card ---
        self.settings_frame = ctk.CTkFrame(self)
        self.settings_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.cfg_label = ctk.CTkLabel(self.settings_frame, text="⚙️ Configuration", font=("Helvetica", 14, "bold"))
        self.cfg_label.pack(anchor="w", padx=15, pady=(10, 10))

        # Count
        self.count_label = ctk.CTkLabel(self.settings_frame, text="Target Amount: 20", font=("Helvetica", 12))
        self.count_label.pack(anchor="w", padx=15)
        self.count_slider = ctk.CTkSlider(self.settings_frame, from_=1, to=1000, command=self.update_count_label)
        self.count_slider.set(20)
        self.count_slider.pack(fill="x", padx=15, pady=(0, 15))

        # Delay
        self.delay_label = ctk.CTkLabel(self.settings_frame, text="Base Delay: 1.0s (Anti-ban variance applied)", font=("Helvetica", 12))
        self.delay_label.pack(anchor="w", padx=15)
        self.delay_slider = ctk.CTkSlider(self.settings_frame, from_=0.1, to=10.0, command=self.update_delay_label)
        self.delay_slider.set(1.0)
        self.delay_slider.pack(fill="x", padx=15, pady=(0, 15))

        # --- Advanced Framework ---
        self.adv_frame = ctk.CTkFrame(self)
        self.adv_frame.pack(fill="x", padx=20, pady=(0, 10))

        # Using a grid inside for better switch alignment
        self.adv_frame.columnconfigure(0, weight=1)
        self.adv_frame.columnconfigure(1, weight=1)

        self.always_on_top_var = ctk.BooleanVar(value=True)
        self.top_switch = ctk.CTkSwitch(self.adv_frame, text="Always on Top", font=("Helvetica", 12), variable=self.always_on_top_var, command=self.toggle_topmost)
        self.top_switch.grid(row=0, column=0, padx=15, pady=(15, 10), sticky="w")

        self.infinite_var = ctk.BooleanVar(value=False)
        self.infinite_switch = ctk.CTkSwitch(self.adv_frame, text="♾️ Infinite Mode", font=("Helvetica", 12), variable=self.infinite_var, command=self.toggle_infinite_mode)
        self.infinite_switch.grid(row=0, column=1, padx=15, pady=(15, 10), sticky="w")

        self.instant_paste_var = ctk.BooleanVar(value=True)
        self.instant_paste_switch = ctk.CTkSwitch(self.adv_frame, text="🚀 Instant Paste", font=("Helvetica", 12), variable=self.instant_paste_var)
        self.instant_paste_switch.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="w")

        # --- Action Footer ---
        self.footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.footer_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))

        self.status_label = ctk.CTkLabel(self.footer_frame, text="Status: Idle", font=("Helvetica", 14, "bold"), text_color="gray")
        self.status_label.pack(pady=(0, 10))

        self.start_btn = ctk.CTkButton(self.footer_frame, text="▶ START SENDER", fg_color="#2b8a3e", hover_color="#237032", font=("Helvetica", 15, "bold"), height=45, corner_radius=8, command=self.start_sending)
        self.start_btn.pack(fill="x", pady=(0, 10))

        self.stop_btn = ctk.CTkButton(self.footer_frame, text="🛑 EMERGENCY STOP", fg_color="#c92a2a", hover_color="#a61e1e", font=("Helvetica", 15, "bold"), height=45, corner_radius=8, command=self.stop_sending, state="disabled")
        self.stop_btn.pack(fill="x")
        
        self.warn_label = ctk.CTkLabel(self.footer_frame, text="Throw mouse to any corner to force stop!", font=("Helvetica", 11), text_color="#c92a2a")
        self.warn_label.pack(pady=(5, 0))


    def toggle_topmost(self):
        self.attributes("-topmost", self.always_on_top_var.get())

    def toggle_infinite_mode(self):
        if self.infinite_var.get():
            self.count_slider.configure(state="disabled")
            self.count_label.configure(text="Target Amount: INFINITE")
        else:
            self.count_slider.configure(state="normal")
            self.update_count_label(self.count_slider.get())

    def update_count_label(self, value):
        if not self.infinite_var.get():
            self.count_label.configure(text=f"Target Amount: {int(value)}")

    def update_delay_label(self, value):
        self.delay_label.configure(text=f"Base Delay: {value:.1f}s (Anti-ban variance applied)")

    def start_sending(self):
        text = self.text_input.get("1.0", "end-1c").strip()
        if not text:
            self.status_label.configure(text="Error: Message cannot be empty", text_color="#c92a2a")
            return

        count = int(self.count_slider.get())
        delay = self.delay_slider.get()
        infinite = self.infinite_var.get()
        use_paste = self.instant_paste_var.get()
        nav_key = self.nav_input.get().strip()

        self.is_running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.text_input.configure(state="disabled")
        self.nav_input.configure(state="disabled")
        
        threading.Thread(target=self.sending_task, args=(text, count, delay, infinite, use_paste, nav_key), daemon=True).start()

    def stop_sending(self):
        self.is_running = False
        self.status_label.configure(text="Status: Stopped by user", text_color="#c92a2a")
        self.reset_buttons()

    def reset_buttons(self):
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.text_input.configure(state="normal")
        self.nav_input.configure(state="normal")

    def sending_task(self, original_text, count, delay, infinite, use_paste, nav_key):
        try:
            # 5 seconds grace period
            for i in range(5, 0, -1):
                if not self.is_running: return
                self.status_label.configure(text=f"Starting in {i}s... Switch to your Chat!", text_color="#f59f00")
                time.sleep(1)

            i = 0
            
            # Identify platform for pasting
            modifier_key = 'command' if sys.platform == 'darwin' else 'ctrl'

            while self.is_running and (infinite or i < count):
                i += 1
                total_str = "∞" if infinite else str(count)
                self.status_label.configure(text=f"Sending {i} / {total_str}...", text_color="#3bc9db")
                
                # Dynamic text replacement!
                current_text = original_text.replace("{count}", str(i))

                if use_paste:
                    pyperclip.copy(current_text)
                    time.sleep(0.05)
                    pyautogui.hotkey(modifier_key, 'v')
                else:
                    # Tiny random variation to mimic human typing
                    type_speed = max(0.001, random.uniform(0.002, 0.015))
                    pyautogui.write(current_text, interval=type_speed)
                
                # Press enter to send
                time.sleep(0.05)
                pyautogui.press("enter")
                
                # JUMP TO NEXT CHAT / TEXT BOX IF CONFIGURED!
                if nav_key:
                    time.sleep(0.1) # micro-rest before switching focus
                    try:
                        if '+' in nav_key:
                            keys = [k.strip().lower() for k in nav_key.split('+')]
                            pyautogui.hotkey(*keys)
                        else:
                            pyautogui.press(nav_key.lower())
                    except Exception:
                        pass # Ignore if user typed an invalid key

                # Dynamic delay
                actual_delay = delay + random.uniform(0.0, 0.3)
                
                # Anti-Spam "Taking a breath" logic
                # Pauses an extra 1.5 to 3.5 seconds every 15 messages
                if i % 15 == 0:
                    actual_delay += random.uniform(1.5, 3.5)

                time.sleep(actual_delay)

            if self.is_running:
                self.status_label.configure(text="Status: Finished successfully!", text_color="#37b24d")
                self.is_running = False
        
        except pyautogui.FailSafeException:
            self.is_running = False
            self.status_label.configure(text="Fail-Safe triggered! (Mouse in corner)", text_color="#c92a2a")
        
        except Exception as e:
            self.is_running = False
            self.status_label.configure(text=f"Error: {str(e)}", text_color="#c92a2a")

        self.reset_buttons()

if __name__ == "__main__":
    app = TextRepeaterApp()
    app.mainloop()
