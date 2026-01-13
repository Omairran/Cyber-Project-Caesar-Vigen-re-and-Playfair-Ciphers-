import tkinter as tk
from tkinter import ttk, messagebox
import time
from logic import CaesarCipher, VigenereCipher, PlayfairCipher

class AdvancedCipherSuiteGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Classical Cipher Suite - Advanced Visualization")
        self.root.geometry("1100x850")
        self.root.configure(bg="#121212")

        # Color Palette
        self.colors = {
            "bg": "#121212",
            "sidebar": "#1e1e1e",
            "card": "#252526",
            "accent": "#007acc",
            "text": "#ffffff",
            "dim_text": "#aaaaaa",
            "success": "#00ff00",
            "highlight": "#ffcc00",
            "matrix_bg": "#2d2d30"
        }

        self.ciphers = {
            "Caesar": CaesarCipher(),
            "Vigenère": VigenereCipher(),
            "Playfair": PlayfairCipher()
        }
        self.current_cipher = tk.StringVar(value="Playfair")
        self.current_mode = tk.StringVar(value="Encrypt")
        self.is_animating = False
        self.is_paused = False
        self.animation_speed = 800 # ms
        self.canvas = None # Initialize to avoid AttributeError

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.colors["sidebar"], height=80)
        header.pack(side="top", fill="x")
        tk.Label(header, text="Classical Cipher Suite - Animation View", font=("Arial", 22, "bold"), 
                 bg=self.colors["sidebar"], fg=self.colors["text"], padx=20, pady=20).pack(side="left")

        # Main Container
        main_container = tk.Frame(self.root, bg=self.colors["bg"])
        main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # -- Left Column: Configuration (Scrollable Sidebar) --
        sidebar_outer = tk.Frame(main_container, bg=self.colors["bg"], width=320)
        sidebar_outer.pack(side="left", fill="y", padx=(0, 20))
        
        # Fixed Start Button at the very top of sidebar
        self.start_btn = tk.Button(sidebar_outer, text="START ANIMATION", command=self.start_animation,
                                   bg=self.colors["accent"], fg="white", font=("Arial", 12, "bold"), 
                                   padx=20, pady=15, borderwidth=0, cursor="hand2")
        self.start_btn.pack(fill="x", pady=(0, 10))

        self.pause_btn = tk.Button(sidebar_outer, text="PAUSE", command=self.toggle_pause,
                                   bg=self.colors["card"], fg="white", font=("Arial", 11, "bold"), 
                                   padx=20, pady=10, borderwidth=0, cursor="hand2", state="disabled")
        self.pause_btn.pack(fill="x", pady=(0, 20))

        # Scrollable Config Area
        sidebar_canvas = tk.Canvas(sidebar_outer, bg=self.colors["bg"], width=300, highlightthickness=0)
        sidebar_scrollbar = tk.Scrollbar(sidebar_outer, orient="vertical", command=sidebar_canvas.yview)
        config_frame = tk.Frame(sidebar_canvas, bg=self.colors["bg"])
        
        config_frame.bind("<Configure>", lambda e: sidebar_canvas.configure(scrollregion=sidebar_canvas.bbox("all")))
        sidebar_canvas.create_window((0, 0), window=config_frame, anchor="nw", width=300)
        sidebar_canvas.configure(yscrollcommand=sidebar_scrollbar.set)
        
        sidebar_canvas.pack(side="left", fill="both", expand=True)
        sidebar_scrollbar.pack(side="right", fill="y")
        
        # Enable MouseWheel scrolling
        def _on_mousewheel(event):
            sidebar_canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        sidebar_canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Cipher Selection
        tk.Label(config_frame, text="Select Cipher", font=("Arial", 11, "bold"), bg=self.colors["bg"], fg=self.colors["dim_text"]).pack(anchor="w", pady=(0, 10))
        for name in self.ciphers.keys():
            rb = tk.Radiobutton(config_frame, text=name, variable=self.current_cipher, value=name,
                                 font=("Arial", 10), bg=self.colors["bg"], fg=self.colors["text"],
                                 selectcolor=self.colors["accent"], activebackground=self.colors["card"],
                                 indicatoron=False, width=30, pady=8, command=self.reset_visualization)
            rb.pack(pady=3)

        # Mode Selection
        tk.Label(config_frame, text="Select Mode", font=("Arial", 11, "bold"), bg=self.colors["bg"], fg=self.colors["dim_text"]).pack(anchor="w", pady=(20, 10))
        mode_frame = tk.Frame(config_frame, bg=self.colors["bg"])
        mode_frame.pack(fill="x")
        for mode in ["Encrypt", "Decrypt"]:
            rb = tk.Radiobutton(mode_frame, text=mode, variable=self.current_mode, value=mode,
                                 font=("Arial", 10), bg=self.colors["bg"], fg=self.colors["text"],
                                 selectcolor=self.colors["accent"], activebackground=self.colors["card"],
                                 indicatoron=False, width=14, pady=8, command=self.reset_visualization)
            rb.pack(side="left", expand=True, padx=2)

        # Animation Speed Adjuster
        speed_header = tk.Frame(config_frame, bg=self.colors["bg"])
        speed_header.pack(fill="x", pady=(25, 5))
        tk.Label(speed_header, text="Animation Speed", font=("Arial", 11, "bold"), bg=self.colors["bg"], fg=self.colors["dim_text"]).pack(side="left")
        self.speed_val_label = tk.Label(speed_header, text="800ms", font=("Arial", 10, "bold"), bg=self.colors["bg"], fg=self.colors["accent"])
        self.speed_val_label.pack(side="right")

        self.speed_slider = tk.Scale(config_frame, from_=50, to=2000, orient="horizontal", 
                                     bg=self.colors["bg"], fg="white", highlightthickness=0, 
                                     troughcolor=self.colors["card"], activebackground=self.colors["accent"],
                                     showvalue=False, command=self.update_speed, length=280)
        self.speed_slider.set(800)
        self.speed_slider.pack(fill="x", padx=10)
        
        speed_labels = tk.Frame(config_frame, bg=self.colors["bg"])
        speed_labels.pack(fill="x")
        tk.Label(speed_labels, text="Fastest", font=("Arial", 8), bg=self.colors["bg"], fg=self.colors["dim_text"]).pack(side="left", padx=10)
        tk.Label(speed_labels, text="Slowest", font=("Arial", 8), bg=self.colors["bg"], fg=self.colors["dim_text"]).pack(side="right", padx=10)

        # Input Area
        tk.Label(config_frame, text="Input Text", font=("Arial", 11, "bold"), bg=self.colors["bg"], fg=self.colors["dim_text"]).pack(anchor="w", pady=(25, 5))
        self.input_entry = tk.Entry(config_frame, font=("Consolas", 12), bg=self.colors["card"], fg="white", borderwidth=0)
        self.input_entry.pack(fill="x", ipady=8, padx=5)

        tk.Label(config_frame, text="Key", font=("Arial", 11, "bold"), bg=self.colors["bg"], fg=self.colors["dim_text"]).pack(anchor="w", pady=(15, 5))
        self.key_entry = tk.Entry(config_frame, font=("Consolas", 12), bg=self.colors["card"], fg="white", borderwidth=0)
        self.key_entry.pack(fill="x", ipady=8, padx=5)

        # Status & Utils
        self.status_label = tk.Label(config_frame, text="Ready", font=("Arial", 10), bg=self.colors["bg"], fg=self.colors["success"])
        self.status_label.pack(pady=20)

        tk.Button(config_frame, text="RESET ALL", command=self.clear_fields,
                  font=("Arial", 9, "bold"), bg="#333", fg="#ff5555", 
                  activebackground="#444", borderwidth=0, cursor="hand2", width=30, pady=5).pack(pady=(10, 20))
        
        # Initialize Visualization Area
        self.setup_vis_area(main_container)

    def update_speed(self, val):
        self.animation_speed = int(val)
        if hasattr(self, 'speed_val_label'):
            self.speed_val_label.config(text=f"{val}ms")

    def toggle_pause(self):
        if not self.is_animating: return
        self.is_paused = not self.is_paused
        btn_text = "RESUME" if self.is_paused else "PAUSE"
        self.pause_btn.config(text=btn_text, bg=self.colors["highlight"] if self.is_paused else self.colors["card"])
        self.status_label.config(text="Paused" if self.is_paused else "Animating...")

    def clear_fields(self):
        self.input_entry.delete(0, tk.END)
        self.key_entry.delete(0, tk.END)
        self.reset_visualization()

    def setup_vis_area(self, main_container):
        # Right Column: Visualization Base
        self.vis_frame = tk.Frame(main_container, bg=self.colors["card"], padx=20, pady=20)
        self.vis_frame.pack(side="left", fill="both", expand=True)

        # -- VIEW 1: Animation View --
        self.anim_view_frame = tk.Frame(self.vis_frame, bg=self.colors["card"])
        self.anim_view_frame.pack(fill="both", expand=True)

        self.vis_title = tk.Label(self.anim_view_frame, text="Algorithm Visualization", font=("Arial", 14, "bold"), 
                                  bg=self.colors["card"], fg=self.colors["text"])
        self.vis_title.pack(anchor="w", pady=(0, 20))

        # Canvas for Drawing
        self.canvas = tk.Canvas(self.anim_view_frame, bg=self.colors["bg"], highlightthickness=0, height=350)
        self.canvas.pack(fill="x", pady=(0, 10))

        # Scrollable Log Area
        log_frame = tk.Frame(self.anim_view_frame, bg=self.colors["bg"])
        log_frame.pack(fill="both", expand=True)
        
        tk.Label(log_frame, text="Transformation Log:", font=("Arial", 10, "bold"), bg=self.colors["bg"], fg=self.colors["dim_text"]).pack(anchor="w")
        
        self.log_text = tk.Text(log_frame, font=("Consolas", 10), bg=self.colors["card"], fg=self.colors["dim_text"], 
                                height=10, borderwidth=0, padx=10, pady=10, state="disabled")
        self.log_text.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

        # -- VIEW 2: Result View (The "Alone" Display) --
        self.res_view_frame = tk.Frame(self.vis_frame, bg=self.colors["card"])
        # Initially hidden

        # Isolated Big Result Card
        self.result_card = tk.Frame(self.res_view_frame, bg=self.colors["matrix_bg"], padx=40, pady=80, 
                                    highlightbackground=self.colors["accent"], highlightthickness=3)
        self.result_card.pack(fill="both", expand=True, pady=40)
        
        tk.Label(self.result_card, text="✨ PROCESSED RESULT ✨", font=("Arial", 12, "bold"), 
                 bg=self.colors["matrix_bg"], fg=self.colors["accent"]).pack(pady=(0, 30))
        
        # Gigantic Result Text Area
        self.result_text = tk.Text(self.result_card, font=("Consolas", 42, "bold"), 
                                   bg=self.colors["matrix_bg"], fg=self.colors["success"], 
                                   height=3, borderwidth=0, wrap="char", highlightthickness=0)
        self.result_text.tag_configure("center", justify='center')
        self.result_text.pack(fill="x", pady=20)
        self.result_text.insert("1.0", "---")
        self.result_text.tag_add("center", "1.0", "end")
        self.result_text.config(state="disabled")

        # Action bar under big result
        action_bar = tk.Frame(self.result_card, bg=self.colors["matrix_bg"])
        action_bar.pack(expand=True, pady=30)

        self.copy_btn = tk.Button(action_bar, text="📋 COPY RESULT", command=self.copy_to_clipboard, 
                                  font=("Arial", 11, "bold"), bg=self.colors["card"], fg="white", 
                                  padx=20, pady=12, borderwidth=0, cursor="hand2")
        self.copy_btn.pack(side="left", padx=15)

        self.swap_btn = tk.Button(action_bar, text="🔄 APPLY TO INPUT", command=self.swap_to_input, 
                                  font=("Arial", 11, "bold"), bg=self.colors["accent"], fg="white", 
                                  padx=20, pady=12, borderwidth=0, cursor="hand2")
        self.swap_btn.pack(side="left", padx=15)

        self.restart_btn = tk.Button(action_bar, text="✖ DISMISS", command=self.reset_visualization, 
                                  font=("Arial", 11, "bold"), bg="#444", fg="white", 
                                  padx=20, pady=12, borderwidth=0, cursor="hand2")
        self.restart_btn.pack(side="left", padx=15)

    def swap_to_input(self):
        """Moves current result to input and toggles mode for quick decryption check."""
        result = self.result_text.get("1.0", tk.END).strip()
        if result and result != "---" and result != "Waiting for animation...":
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, result)
            
            # Toggle Mode
            current = self.current_mode.get()
            new_mode = "Decrypt" if current == "Encrypt" else "Encrypt"
            self.current_mode.set(new_mode)
            
            self.reset_visualization()
            messagebox.showinfo("Swapped", f"Moved result to input and switched to {new_mode} mode.")

    def copy_to_clipboard(self):
        self.root.clipboard_clear()
        content = self.result_text.get("1.0", tk.END).strip()
        if content == "---" or content == "Waiting for animation...": return
        self.root.clipboard_append(content)
        messagebox.showinfo("Success", "Result copied to clipboard!")

    def reset_visualization(self):
        if not hasattr(self, 'canvas') or self.canvas is None:
            return
            
        self.canvas.delete("all")
        self.is_animating = False
        
        # Show Animation View, Hide Result View
        if hasattr(self, 'res_view_frame') and hasattr(self, 'anim_view_frame'):
            self.res_view_frame.pack_forget()
            self.anim_view_frame.pack(fill="both", expand=True)

        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", "---")
        self.result_text.tag_add("center", "1.0", "end")
        self.result_text.config(fg=self.colors["success"], state="disabled")
        
        self.status_label.config(text="Ready")
        
        # Update Dynamic Labels
        mode = self.current_mode.get()
        self.vis_title.config(text=f"{self.current_cipher.get()} - {mode} Visualization")
        self.start_btn.config(text=f"START {mode.upper()}")
        
        self.log_text.config(state="normal")
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state="disabled")
        
        self.draw_base_layout()

    def set_result(self, text):
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", text)
        self.result_text.tag_add("center", "1.0", "end")
        self.result_text.config(state="disabled")

    def append_result(self, char):
        self.result_text.config(state="normal")
        # If it's the first character, clear the placeholder
        content = self.result_text.get("1.0", tk.END).strip()
        if content == "---":
            self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, char)
        self.result_text.tag_add("center", "1.0", "end")
        self.result_text.see(tk.END)
        self.result_text.config(state="disabled")

    def complete_animation(self, final_str):
        self.is_animating = False
        self.is_paused = False
        self.pause_btn.config(state="disabled", text="PAUSE")
        self.status_label.config(text="Animation Complete")
        
        # Switch to Result View: Hides canvas and log
        self.anim_view_frame.pack_forget()
        self.res_view_frame.pack(fill="both", expand=True)

        # Playfair Decryption Cleanup
        if self.current_cipher.get() == "Playfair" and self.current_mode.get() == "Decrypt":
            if final_str.endswith("X"):
                final_str = final_str[:-1]
        
        self.set_result(final_str)
        # Flash result label to signal completion
        self.result_text.config(state="normal")
        self.result_text.config(fg="white")
        self.root.after(200, lambda: self.result_text.config(fg=self.colors["success"], state="disabled"))
        self.log_history("Done: All transformations complete.")

    def draw_base_layout(self):
        cipher_name = self.current_cipher.get()
        if cipher_name == "Playfair":
            self.draw_matrix_base()
        else:
            self.draw_alphabet_base()

    def draw_matrix_base(self):
        cell_size = 50
        offset_x, offset_y = 50, 40
        self.matrix_cells = {}
        for r in range(5):
            for c in range(5):
                x1, y1 = offset_x + c * cell_size, offset_y + r * cell_size
                x2, y2 = x1 + cell_size, y1 + cell_size
                rect = self.canvas.create_rectangle(x1, y1, x2, y2, outline="#444444", fill=self.colors["matrix_bg"])
                text = self.canvas.create_text(x1 + cell_size/2, y1 + cell_size/2, text="", 
                                               fill="white", font=("Arial", 14, "bold"))
                self.matrix_cells[(r, c)] = (rect, text)

    def draw_alphabet_base(self):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        cell_size = 30
        y1, y2 = 80, 140
        self.alpha_static = []
        self.alpha_ribbon = []
        
        # Static Alphabet
        for i, char in enumerate(alphabet):
            x = 40 + i * cell_size
            r = self.canvas.create_rectangle(x, y1, x + cell_size, y1 + cell_size, outline="#444444")
            t = self.canvas.create_text(x + cell_size/2, y1 + cell_size/2, text=char, fill="white", font=("Arial", 10))
            self.alpha_static.append((r, t))

        # Ribbon Alphabet
        for i, char in enumerate(alphabet):
            x = 40 + i * cell_size
            r = self.canvas.create_rectangle(x, y2, x + cell_size, y2 + cell_size, outline="#444444", fill=self.colors["matrix_bg"])
            t = self.canvas.create_text(x + cell_size/2, y2 + cell_size/2, text=char, fill="white", font=("Arial", 10))
            self.alpha_ribbon.append((r, t))

    def start_animation(self):
        if self.is_animating: return
        
        text = self.input_entry.get().strip()
        key = self.key_entry.get().strip()
        cipher_name = self.current_cipher.get()
        mode = self.current_mode.get()

        if not text or not key:
            messagebox.showwarning("Warning", "Please provide both text and key.")
            return

        self.reset_visualization()
        self.is_animating = True
        self.is_paused = False
        self.pause_btn.config(state="normal", text="PAUSE", bg=self.colors["card"])
        self.set_result("") # Start empty for reveal

        cipher = self.ciphers[cipher_name]
        try:
            if mode == "Encrypt":
                res = cipher.encrypt(text, key)
            else:
                res = cipher.decrypt(text, key)
                
            if cipher_name == "Playfair":
                self.animate_playfair(cipher._animation_data, res)
            else:
                self.animate_standard(cipher_name, text, key, res, mode)
        except Exception as e:
            self.is_animating = False
            self.set_result("Error occurred")
            messagebox.showerror("Error", str(e))

    def animate_playfair(self, data, final_str):
        matrix = data["matrix"]
        steps = data["steps"]
        mode = self.current_mode.get()
        
        for r in range(5):
            for c in range(5):
                self.canvas.itemconfig(self.matrix_cells[(r, c)][1], text=matrix[r][c])

        def step_anim(idx):
            if not self.is_animating or idx >= len(steps):
                self.complete_animation(final_str)
                return

            for r_c in self.matrix_cells.values():
                self.canvas.itemconfig(r_c[0], fill=self.colors["matrix_bg"])

            step = steps[idx]
            self.status_label.config(text=f"Pair {idx+1}: {step['pair']} -> {step['result']} ({step['rule']})")
            coords = step["coords"]
            
            # Original letters in yellow
            self.canvas.itemconfig(self.matrix_cells[coords[0]][0], fill="#ff9900")
            self.canvas.itemconfig(self.matrix_cells[coords[1]][0], fill="#ff9900")
            
            def highlight_target():
                if self.is_paused:
                    self.root.after(200, highlight_target)
                    return
                self.canvas.itemconfig(self.matrix_cells[coords[2]][0], fill="#00aa00")
                self.canvas.itemconfig(self.matrix_cells[coords[3]][0], fill="#00aa00")
                
                # Update revealed result
                self.append_result(step["result"])
                
                self.log_history(f"Step {idx+1} ({mode}): {step['pair']} -> {step['result']} ({step['rule']})")
                
                def wait_for_next():
                    if self.is_paused:
                        self.root.after(200, wait_for_next)
                    else:
                        step_anim(idx+1)
                
                self.root.after(self.animation_speed, wait_for_next)

            if self.is_paused:
                self.root.after(200, lambda: step_anim(idx)) # Retry same index
            else:
                self.root.after(400, highlight_target)

        step_anim(0)

    def animate_standard(self, name, text, key, result, mode):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        cell_size = 30
        y1, y2 = 80, 140

        # Special Vigenere Visualization Area (Grid/Array style)
        if name == "Vigenère":
            label_y = 200
            grid_y1 = 230
            grid_y2 = 255
            cell_w = 25
            
            self.canvas.create_text(40, label_y, text=f"Alignment Array ({mode}):", fill=self.colors["dim_text"], anchor="w", font=("Arial", 10, "bold"))
            self.canvas.create_text(20, grid_y1 + 12, text="T:", fill=self.colors["dim_text"], anchor="w", font=("Arial", 8, "bold"))
            self.canvas.create_text(20, grid_y2 + 12, text="K:", fill=self.colors["dim_text"], anchor="w", font=("Arial", 8, "bold"))

            self.vig_text_cells = []
            self.vig_key_cells = []
            
            # Draw array of cells for input text and repeated key
            for i, char in enumerate(text):
                # We limit to what fits roughly on screen to avoid messy overflow
                if i > 25: break 
                x = 40 + i * cell_w
                
                # Text Row Cell
                r1 = self.canvas.create_rectangle(x, grid_y1, x + cell_w, grid_y1 + 22, outline="#444", fill=self.colors["matrix_bg"])
                t1 = self.canvas.create_text(x + cell_w/2, grid_y1 + 11, text=char.upper(), fill="white", font=("Consolas", 10))
                self.vig_text_cells.append((r1, t1, x))
                
                # Key Row Cell
                k_char = key[i % len(key)].upper() if char.isalpha() else " "
                r2 = self.canvas.create_rectangle(x, grid_y2, x + cell_w, grid_y2 + 22, outline="#444", fill=self.colors["matrix_bg"])
                # Key text starts as empty string to 'hide' initially
                t2 = self.canvas.create_text(x + cell_w/2, grid_y2 + 11, text="", fill=self.colors["success"], font=("Consolas", 10, "bold"))
                self.vig_key_cells.append((r2, t2, k_char))

        def update_ribbon(shift):
            if mode == "Decrypt": shift = -shift
            shifted_alpha = alphabet[shift % 26:] + alphabet[:shift % 26]
            for i, char in enumerate(shifted_alpha):
                self.canvas.itemconfig(self.alpha_ribbon[i][1], text=char)

        def step_anim(idx, result_idx=0):
            if idx >= len(text):
                self.complete_animation(result)
                return

            char = text[idx].upper()
            if not char.isalpha():
                if self.is_paused:
                    self.root.after(200, lambda: step_anim(idx, result_idx))
                    return
                # For non-alpha, highlight text box if it exists
                if name == "Vigenère" and idx < len(self.vig_text_cells):
                    self.canvas.itemconfig(self.vig_text_cells[idx][0], fill=self.colors["sidebar"])

                self.append_result(text[idx])
                self.root.after(50, lambda: step_anim(idx+1, result_idx))
                return

            if name == "Caesar":
                shift = int(key) % 26
                display_shift = shift if mode == "Encrypt" else -shift
                self.status_label.config(text=f"Letter {idx+1}: {char} | Shift: {display_shift}")
            else: # Vigenere
                result_idx_val = result_idx
                k_char = key[result_idx_val % len(key)].upper()
                shift = (ord(k_char) - ord('A')) % 26
                display_shift = shift if mode == "Encrypt" else -shift
                self.status_label.config(text=f"Letter {idx+1}: {char} | Key: {k_char} (Shift: {display_shift})")
                
                # Highlight Grid Cells
                if idx < len(self.vig_text_cells):
                    # Reset all previous
                    for cell_idx in range(len(self.vig_text_cells)):
                        self.canvas.itemconfig(self.vig_text_cells[cell_idx][0], fill=self.colors["matrix_bg"])
                        self.canvas.itemconfig(self.vig_key_cells[cell_idx][0], fill=self.colors["matrix_bg"])
                    
                    # Current alignment
                    self.canvas.itemconfig(self.vig_text_cells[idx][0], fill=self.colors["highlight"])
                    self.canvas.itemconfig(self.vig_key_cells[idx][0], fill=self.colors["highlight"])
                    # Reveal the key letter for this step
                    self.canvas.itemconfig(self.vig_key_cells[idx][1], text=self.vig_key_cells[idx][2])
            
            # Draw Numeric Shift Indicator (+N/-N)
            shift_val = display_shift
            sign = "+" if shift_val >= 0 else "-"
            shift_text = f"{sign}{abs(shift_val)}"
            shift_indicator = self.canvas.create_text(40 + (ord(char)-ord('A'))*cell_size + cell_size/2, 
                                                    (y1+y2)/2, text=shift_text, 
                                                    fill=self.colors["highlight"], font=("Arial", 11, "bold"))
            
            update_ribbon(shift)
            
            orig_idx = ord(char) - ord('A')
            x_pos = 40 + orig_idx * cell_size
            
            high1 = self.canvas.create_rectangle(x_pos, y1, x_pos + cell_size, y1 + cell_size, outline=self.colors["highlight"], width=3)
            high2 = self.canvas.create_rectangle(x_pos, y2, x_pos + cell_size, y2 + cell_size, outline=self.colors["success"], width=3)
            
            new_char = result[result_idx]
            
            def next_step():
                if self.is_paused:
                    self.root.after(200, next_step)
                    return
                    
                self.canvas.delete(high1)
                self.canvas.delete(high2)
                if 'shift_indicator' in locals():
                    self.canvas.delete(shift_indicator)
                self.append_result(new_char)
                self.log_history(f"[{mode}] '{char}' -> '{new_char}'")
                
                def wait_for_next():
                    if self.is_paused:
                        self.root.after(200, wait_for_next)
                    else:
                        step_anim(idx+1, result_idx+1)
                
                self.root.after(self.animation_speed, wait_for_next)

            if self.is_paused:
                self.root.after(200, lambda: step_anim(idx, result_idx))
            else:
                self.root.after(self.animation_speed, next_step)

        step_anim(0)

    def log_history(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, f"• {message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = AdvancedCipherSuiteGUI(root)
    app.reset_visualization()
    root.mainloop()
