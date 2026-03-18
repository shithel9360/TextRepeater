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
        self.targets = []

        # --- Header ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(fill="x", padx=20, pady=(15, 5))
        
        self.title_label = ctk.CTkLabel(self.header_frame, text="⚡ Text Sender Pro", font=("Helvetica", 28, "bold"), text_color="#1f6aa5")
        self.title_label.pack(anchor="center")
        
        self.subtitle_label = ctk.CTkLabel(self.header_frame, text="Automated & Untraceable Messaging", font=("Helvetica", 12), text_color="gray")
        self.subtitle_label.pack(anchor="center")

        # --- Message Card ---
        self.msg_frame = ctk.CTkFrame(self)
        self.msg_frame.pack(fill="x", padx=20, pady=(5, 10))

        self.text_label = ctk.CTkLabel(self.msg_frame, text="📝 Message Payload", font=("Helvetica", 14, "bold"))
        self.text_label.pack(anchor="w", padx=15, pady=(10, 5))
        
        self.hint_label = ctk.CTkLabel(self.msg_frame, text="Tip: Use {count} to inject message numbers into the text.", font=("Helvetica", 11), text_color="gray")
        self.hint_label.pack(anchor="w", padx=15, pady=(0, 5))

        self.text_input = ctk.CTkTextbox(self.msg_frame, height=90, border_width=1, border_color="#333333")
        self.text_input.pack(fill="x", padx=15, pady=(0, 15))


        # --- Target Recorder Card ---
        self.target_frame = ctk.CTkFrame(self)
        self.target_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.target_label = ctk.CTkLabel(self.target_frame, text="🎯 Multi-Target Bomber (Optional)", font=("Helvetica", 14, "bold"))
        self.target_label.pack(anchor="w", padx=15, pady=(10, 0))
        
        self.target_hint = ctk.CTkLabel(self.target_frame, text="Record the locations of multiple chat boxes (Insta, FB, WP).\nThe bot will automatically click and cycle through all of them!", font=("Helvetica", 11), text_color="gray", justify="left")
        self.target_hint.pack(anchor="w", padx=15, pady=(2, 5))

        self.target_status = ctk.CTkLabel(self.target_frame, text="Recorded Chat Boxes: 0", font=("Helvetica", 13, "bold"), text_color="#f59f00")
        self.target_status.pack(anchor="w", padx=15, pady=(0, 5))

        self.target_btn_frame = ctk.CTkFrame(self.target_frame, fg_color="transparent")
        self.target_btn_frame.pack(fill="x", padx=15, pady=(0, 15))

        self.record_btn = ctk.CTkButton(self.target_btn_frame, text="[+] Record Box", fg_color="#1f6aa5", width=120, height=32, font=("Helvetica", 12, "bold"), command=self.start_record_target)
        self.record_btn.pack(side="left", padx=(0, 10))

        self.clear_btn = ctk.CTkButton(self.target_btn_frame, text="[x] Clear", fg_color="#c92a2a", hover_color="#a61e1e", width=60, height=32, font=("Helvetica", 12, "bold"), command=self.clear_targets)
        self.clear_btn.pack(side="left")

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
        self.delay_label = ctk.CTkLabel(self.settings_frame, text="Base Delay: 1.0s (Anti-ban variance automatically added)", font=("Helvetica", 12))
        self.delay_label.pack(anchor="w", padx=15)
        self.delay_slider = ctk.CTkSlider(self.settings_frame, from_=0.1, to=10.0, command=self.update_delay_label)
        self.delay_slider.set(1.0)
        self.delay_slider.pack(fill="x", padx=15, pady=(0, 15))

        # --- Advanced Switches ---
        self.adv_frame = ctk.CTkFrame(self)
        self.adv_frame.pack(fill="x", padx=20, pady=(0, 5))

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
        self.footer_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.status_label = ctk.CTkLabel(self.footer_frame, text="Status: Idle", font=("Helvetica", 14, "bold"), text_color="gray")
        self.status_label.pack(pady=(0, 10))

        self.start_btn = ctk.CTkButton(self.footer_frame, text="▶ START SENDER", fg_color="#2b8a3e", hover_color="#237032", font=("Helvetica", 15, "bold"), height=45, corner_radius=8, command=self.start_sending)
        self.start_btn.pack(fill="x", pady=(0, 10))

        self.stop_btn = ctk.CTkButton(self.footer_frame, text="🛑 EMERGENCY STOP", fg_color="#c92a2a", hover_color="#a61e1e", font=("Helvetica", 15, "bold"), height=45, corner_radius=8, command=self.stop_sending, state="disabled")
        self.stop_btn.pack(fill="x")
        
        self.warn_label = ctk.CTkLabel(self.footer_frame, text="Throw mouse to any corner to force stop!", font=("Helvetica", 11), text_color="#c92a2a")
        self.warn_label.pack(pady=(5, 0))


    # --- Target Recorder Logic ---
    def start_record_target(self):
        self.record_btn.configure(state="disabled")
        threading.Thread(target=self.record_target_task, daemon=True).start()

    def record_target_task(self):
        try:
            for i in range(3, 0, -1):
                self.target_status.configure(text=f"Point mouse at chat box in {i}s...", text_color="#f59f00")
                time.sleep(1)
            
            x, y = pyautogui.position()
            self.targets.append((x, y))
            self.target_status.configure(text=f"Recorded Chat Boxes: {len(self.targets)}", text_color="#37b24d")
        except Exception as e:
            self.target_status.configure(text=f"Error recording!", text_color="#c92a2a")
        
        self.record_btn.configure(state="normal")

    def clear_targets(self):
        self.targets = []
        self.target_status.configure(text="Recorded Chat Boxes: 0", text_color="#f59f00")

    # --- UI Callbacks ---
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
        self.delay_label.configure(text=f"Base Delay: {value:.1f}s")


    # --- Spam Logic ---
    def start_sending(self):
        text = self.text_input.get("1.0", "end-1c").strip()
        if not text:
            self.status_label.configure(text="Error: Message cannot be empty", text_color="#c92a2a")
            return

        count = int(self.count_slider.get())
        delay = self.delay_slider.get()
        infinite = self.infinite_var.get()
        use_paste = self.instant_paste_var.get()

        self.is_running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.text_input.configure(state="disabled")
        self.record_btn.configure(state="disabled")
        self.clear_btn.configure(state="disabled")
        
        threading.Thread(target=self.sending_task, args=(text, count, delay, infinite, use_paste), daemon=True).start()

    def stop_sending(self):
        self.is_running = False
        self.status_label.configure(text="Status: Stopped by user", text_color="#c92a2a")
        self.reset_buttons()

    def reset_buttons(self):
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.text_input.configure(state="normal")
        self.record_btn.configure(state="normal")
        self.clear_btn.configure(state="normal")

    def sending_task(self, original_text, count, delay, infinite, use_paste):
        try:
            has_targets = len(self.targets) > 0
            # 5 seconds grace period ONLY if we don't have auto-click targets.
            # If we have targets, it will click them itself, so we just give 2 seconds heads up.
            start_delay = 2 if has_targets else 5
            for i in range(start_delay, 0, -1):
                if not self.is_running: return
                msg = f"Bot starting in {i}s..." if has_targets else f"Starting in {i}s... Switch to Chat!"
                self.status_label.configure(text=msg, text_color="#f59f00")
                time.sleep(1)

            i = 0
            target_idx = 0
            
            # Identify platform for pasting
            modifier_key = 'command' if sys.platform == 'darwin' else 'ctrl'

            while self.is_running and (infinite or i < count):
                i += 1
                total_str = "∞" if infinite else str(count)
                self.status_label.configure(text=f"Sending {i} / {total_str}...", text_color="#3bc9db")
                
                # Dynamic text replacement!
                current_text = original_text.replace("{count}", str(i))

                # IF TARGETS EXIST, AUTO CLICK FIRST
                if has_targets:
                    tx, ty = self.targets[target_idx]
                    pyautogui.click(tx, ty)
                    time.sleep(0.2)
                    pyautogui.click(tx, ty)
                    time.sleep(0.4) # Crucial on Mac: first click focuses the App, second click focuses the Text Box
                    target_idx = (target_idx + 1) % len(self.targets) # cycle exactly like a loop

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

                # Dynamic delay
                actual_delay = delay + random.uniform(0.0, 0.3)
                
                # Anti-Spam "Taking a breath" logic
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
