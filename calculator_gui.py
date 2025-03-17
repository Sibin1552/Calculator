import tkinter as tk
from tkinter import filedialog, messagebox, Menu
import math
import re
from fpdf import FPDF

class ProfessionalCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Professional Calculator")
        self.root.geometry("600x750")
        self.root.resizable(True, True)
        self.expression = ""
        self.history = []
        self.memory = 0
        self.current_theme = "light"  # Default theme
        self.create_widgets()
        self.root.bind("<Key>", self.on_key_press)

    def create_widgets(self):
        self.input_var = tk.StringVar()
        self.entry = tk.Entry(self.root, textvariable=self.input_var, font=("Arial", 24), bd=5, relief=tk.GROOVE, justify='right', bg="#f9f9f9")
        self.entry.grid(row=0, column=0, columnspan=5, padx=10, pady=10, ipadx=8, ipady=8, sticky="ew")
        self.entry.bind("<Return>", lambda event: self.on_button_click("="))
        self.entry.bind("<BackSpace>", lambda event: self.on_button_click("⌫"))

        # Three-dash menu button
        self.menu_button = tk.Menubutton(self.root, text="≡", font=("Arial", 12, "bold"), relief=tk.RAISED)
        self.menu_button.grid(row=7, column=0, sticky="ew")
        menu = Menu(self.menu_button, tearoff=0)
        menu.add_command(label="History", command=self.show_history)
        menu.add_command(label="Save as PDF", command=self.save_pdf)
        self.menu_button.configure(menu=menu)

        # Options button
        self.options_button = tk.Button(self.root, text="Options", font=("Arial", 12, "bold"), relief=tk.RAISED, command=self.options_function)
        self.options_button.grid(row=7, column=1, columnspan=2, sticky="ew")

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3), ('√', 1, 4),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3), ('^', 2, 4),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3), ('log', 3, 4),
            ('0', 4, 0), ('.', 4, 1), ('+', 4, 2), ('=', 4, 3), ('sin', 4, 4),
            ('C', 5, 0), ('cos', 5, 1), ('tan', 5, 2), ('π', 5, 3), ('e', 5, 4),
            ('⌫', 6, 0), ('M+', 6, 1), ('M-', 6, 2), ('MR', 6, 3), ('MC', 6, 4)
        ]
        
        self.buttons = {}
        for btn_text, row, col in buttons:
            btn_widget = tk.Button(self.root, text=btn_text, font=("Arial", 16, "bold"), bg="#dfe6e9", relief=tk.RAISED, command=lambda x=btn_text: self.on_button_click(x))
            btn_widget.grid(row=row, column=col, sticky="nsew", padx=5, ipady=10)
            self.buttons[btn_text] = btn_widget
        
        for i in range(8):
            self.root.grid_rowconfigure(i, weight=1, minsize=80)
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1, minsize=80)
    
    def options_function(self):
        options_window = tk.Toplevel(self.root)
        options_window.title("Options")
        options_window.geometry("300x200")
        tk.Button(options_window, text="Clear History", command=self.clear_history).pack(pady=10)
        tk.Button(options_window, text="Change Theme", command=self.change_theme).pack(pady=10)
        tk.Button(options_window, text="About", command=self.show_about).pack(pady=10)

    def clear_history(self):
        self.history.clear()
        messagebox.showinfo("Info", "History cleared.")

    def change_theme(self):
        self.current_theme = "dark" if self.current_theme == "light" else "light"
        self.apply_theme()

    def apply_theme(self):
        if self.current_theme == "dark":
            self.root.configure(bg="#2d2d2d")
            self.entry.configure(bg="#3d3d3d", fg="#ffffff")
            for btn in self.buttons.values():
                btn.configure(bg="#5d5d5d", fg="#ffffff")
        else:
            self.root.configure(bg="#f0f0f0")
            self.entry.configure(bg="#f9f9f9", fg="#000000")
            for btn in self.buttons.values():
                btn.configure(bg="#dfe6e9", fg="#000000")

    def show_about(self):
        messagebox.showinfo("About", "Professional Calculator\nVersion 1.0")

    def on_button_click(self, char):
        try:
            if char == "C":
                self.expression = ""
            elif char == "=":
                expr = self.expression.replace("^", "**").replace("π", str(math.pi)).replace("e", str(math.e))
                expr = re.sub(r'√(\d+)', r'math.sqrt(\1)', expr)
                expr = re.sub(r'log(\d+)', r'math.log10(\1)', expr)
                expr = re.sub(r'sin(\d+)', r'math.sin(math.radians(\1))', expr)
                expr = re.sub(r'cos(\d+)', r'math.cos(math.radians(\1))', expr)
                expr = re.sub(r'tan(\d+)', r'math.tan(math.radians(\1))', expr)
                result = str(eval(expr))
                self.history.append(self.expression + " = " + result)
                self.expression = result
            elif char == "⌫":
                self.expression = self.expression[:-1]
            elif char == "M+":
                self.memory = float(self.expression) if self.expression else self.memory
            elif char == "M-":
                self.memory -= float(self.expression) if self.expression else 0
            elif char == "MR":
                self.expression = str(self.memory)
            elif char == "MC":
                self.memory = 0
            else:
                self.expression += char
            self.input_var.set(self.expression)
        except ZeroDivisionError:
            messagebox.showerror("Math Error", "Cannot divide by zero")
            self.expression = ""
            self.input_var.set("")
        except Exception as e:
            messagebox.showerror("Error", f"Invalid Input: {e}")
            self.expression = ""
            self.input_var.set("")

    def on_key_press(self, event):
        key = event.char
        if key.isdigit() or key in "+-*/.^()":
            self.on_button_click(key)
        elif key == "\r":
            self.on_button_click("=")
        elif key == "\x08":
            self.on_button_click("⌫")

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Calculation History")
        history_window.geometry("400x300")
        history_listbox = tk.Listbox(history_window, font=("Arial", 12), width=50, height=15)
        history_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        for calc in self.history[-10:]:
            history_listbox.insert(tk.END, calc)

    def save_pdf(self):
        if not self.history:
            return
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=14)
            pdf.cell(200, 10, "Calculation History", ln=True, align="C")
            for calc in self.history:
                pdf.cell(200, 10, calc, ln=True)
            pdf.output(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    calculator = ProfessionalCalculator(root)
    root.mainloop()