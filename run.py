from main_gui import AdvancedCipherSuiteGUI
import tkinter as tk

if __name__ == "__main__":
    print("Starting Advanced Classical Cipher Suite...")
    root = tk.Tk()
    app = AdvancedCipherSuiteGUI(root)
    print("GUI initialized. Opening window...")
    root.mainloop()
    print("Application closed.")
