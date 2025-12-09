import tkinter as tk
from tkinter import messagebox
import sys
import io

# Спроба імпорту модулів
try:
    import data_analyze
    import lego_analysis
    import bayesian_analysis
except ImportError as e:
    print(f"Помилка імпорту модулів: {e}")
    print("Переконайтеся, що файли data_analyze.py, lego_analysis.py та bayesian_analysis.py знаходяться " \
          "в тій же директорії, що й main.py.")

class LegoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("LEGO Data Analytics Project")
        self.root.geometry("1000x650")
        
        self.colors = {
            "sidebar_bg": "#2c3e50",  
            "sidebar_fg": "#ecf0f1",  
            "btn_bg": "#34495e",     
            "btn_hover": "#1abc9c",   
            "btn_fg": "#ffffff",      
            "danger_bg": "#c0392b",   
            "danger_hover": "#e74c3c",
            "console_bg": "#1e1e1e",  
            "console_fg": "#00ff00"   
        }

        self.sidebar = tk.Frame(root, width=250, bg=self.colors["sidebar_bg"])
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)
        self.sidebar.pack_propagate(False)

        title_label = tk.Label(self.sidebar, text="LEGO PROJECT", 
                               bg=self.colors["sidebar_bg"], fg=self.colors["sidebar_fg"],
                               font=("Segoe UI", 18, "bold"))
        title_label.pack(pady=(40, 50))

        self.create_custom_btn("1. Описова статистика", self.run_stats)
        self.create_custom_btn("2. Графіки розподілу", self.run_graphs)
        self.create_custom_btn("3. Аналіз Байєса", self.run_bayes)

        tk.Frame(self.sidebar, bg=self.colors["sidebar_bg"], height=20).pack()

        self.create_custom_btn("ОЧИСТИТИ КОНСОЛЬ", self.clear_console, is_danger=True)

        self.main_area = tk.Frame(root, bg="#ecf0f1")
        self.main_area.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        lbl_cons = tk.Label(self.main_area, text="System Output Log", 
                            bg="#ecf0f1", fg="#7f8c8d", 
                            font=("Consolas", 10, "bold"), anchor="w")
        lbl_cons.pack(fill=tk.X, padx=10, pady=(10, 0))

        self.text_area = tk.Text(self.main_area, bg=self.colors["console_bg"], 
                                 fg=self.colors["console_fg"],
                                 font=("Consolas", 11), bd=0, padx=10, pady=10)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=(5, 10))

    def create_custom_btn(self, text, command_func, is_danger=False):
        """
        Створює Label, який виглядає і працює як кнопка.
        """
        bg_color = self.colors["danger_bg"] if is_danger else self.colors["btn_bg"]
        hover_color = self.colors["danger_hover"] if is_danger else self.colors["btn_hover"]
        
        container = tk.Frame(self.sidebar, bg=self.colors["sidebar_bg"], pady=2)
        container.pack(fill=tk.X)

        btn = tk.Label(container, text=text, 
                       bg=bg_color, fg=self.colors["btn_fg"],
                       font=("Segoe UI", 11), cursor="hand2",
                       pady=12, padx=20, anchor="w") 
        
        btn.pack(fill=tk.X, padx=10)

        btn.bind("<Button-1>", lambda e: command_func())
        btn.bind("<Enter>", lambda e: btn.config(bg=hover_color))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))

    def redirect_output(self, func):
        captured_output = io.StringIO()
        original_stdout = sys.stdout
        try:
            sys.stdout = captured_output
            func()
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            sys.stdout = original_stdout
        
        output_text = captured_output.getvalue()
        self.text_area.insert(tk.END, f">>> RUNNING {func.__name__}...\n", "info")
        self.text_area.insert(tk.END, output_text)
        self.text_area.insert(tk.END, "-"*60 + "\n\n")
        self.text_area.see(tk.END)

    def run_stats(self):
        self.redirect_output(data_analyze.run_full_analysis)

    def run_graphs(self):
        self.text_area.insert(tk.END, ">>> Opening Matplotlib charts...\n")
        self.redirect_output(lego_analysis.show_graphs)

    def run_bayes(self):
        self.redirect_output(bayesian_analysis.run_bayes)

    def clear_console(self):
        self.text_area.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = LegoApp(root)
    root.mainloop()