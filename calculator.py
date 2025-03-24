import tkinter as tk
from tkinter import messagebox, Menu, colorchooser, filedialog
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
        self.undo_stack = []
        self.redo_stack = []
        # Default light theme
        self.current_theme = {
            "bg": "#f9f9f9", 
            "fg": "#000000", 
            "btn_bg": "#dfe6e9", 
            "btn_fg": "#000000",
            "entry_bg": "#ffffff",
            "entry_fg": "#000000"
        }
        # Dark theme colors
        self.dark_theme = {
            "bg": "#2d3436", 
            "fg": "#ffffff", 
            "btn_bg": "#636e72", 
            "btn_fg": "#ffffff",
            "entry_bg": "#2d3436",
            "entry_fg": "#ffffff"
        }
        self.is_dark_mode = False

        self.create_widgets()
        self.root.bind("<Key>", self.on_key_press)

    def create_widgets(self):
        # Three-dash menu at the top-left corner
        self.menu_button = tk.Menubutton(self.root, text="≡", font=("Arial", 14, "bold"), relief=tk.RAISED)
        self.menu_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        menu = Menu(self.menu_button, tearoff=0)
        menu.add_command(label="History", command=self.show_history)
        menu.add_command(label="Save as PDF", command=self.save_history_as_pdf)
        menu.add_command(label="Theme", command=self.change_theme)
        menu.add_command(label="Dark Mode", command=self.toggle_dark_mode)
        self.menu_button.configure(menu=menu)

        # Entry field
        self.input_var = tk.StringVar()
        self.entry = tk.Entry(self.root, textvariable=self.input_var, font=("Arial", 24), bd=5, relief=tk.GROOVE, 
                              justify='right', bg=self.current_theme["entry_bg"], fg=self.current_theme["entry_fg"])
        self.entry.grid(row=1, column=0, columnspan=5, padx=10, pady=10, ipadx=8, ipady=8, sticky="ew")
        self.entry.bind("<Return>", lambda event: self.on_button_click("="))
        self.entry.bind("<BackSpace>", lambda event: self.on_button_click("⌫"))

        buttons = [
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3), ('Undo', 2, 4),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3), ('Redo', 3, 4),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3), ('M+', 4, 4),
            ('0', 5, 0), ('.', 5, 1), ('+', 5, 2), ('=', 5, 3), ('M-', 5, 4),
            ('C', 6, 0), ('MRC', 6, 1), ('MC', 6, 2), ('Exit', 6, 3)
        ]

        self.buttons = {}
        for btn_text, row, col in buttons:
            btn_widget = tk.Button(self.root, text=btn_text, font=("Arial", 16, "bold"), 
                                   bg=self.current_theme["btn_bg"], fg=self.current_theme["btn_fg"], 
                                   relief=tk.RAISED, command=lambda x=btn_text: self.on_button_click(x))
            btn_widget.grid(row=row, column=col, sticky="nsew", padx=5, ipady=10)
            self.buttons[btn_text] = btn_widget
        
        for i in range(7):
            self.root.grid_rowconfigure(i, weight=1, minsize=80)
        for i in range(5):
            self.root.grid_columnconfigure(i, weight=1, minsize=80)

    def toggle_dark_mode(self):
        """Toggle between dark and light theme"""
        self.is_dark_mode = not self.is_dark_mode
        if self.is_dark_mode:
            self.current_theme = self.dark_theme.copy()
        else:
            # Reset to default light theme
            self.current_theme = {
                "bg": "#f9f9f9", 
                "fg": "#000000", 
                "btn_bg": "#dfe6e9", 
                "btn_fg": "#000000",
                "entry_bg": "#ffffff",
                "entry_fg": "#000000"
            }
        self.apply_theme()

    def on_button_click(self, char):
        try:
            if char == "C":
                self.undo_stack.append(self.expression)
                self.expression = ""
            elif char == "=":
                self.undo_stack.append(self.expression)
                result = str(eval(self.expression))
                self.history.append(self.expression + " = " + result)
                self.expression = result
            elif char == "⌫":
                self.undo_stack.append(self.expression)
                self.expression = self.expression[:-1]
            elif char == "Undo":
                if self.undo_stack:
                    self.redo_stack.append(self.expression)
                    self.expression = self.undo_stack.pop()
            elif char == "Redo":
                if self.redo_stack:
                    self.undo_stack.append(self.expression)
                    self.expression = self.redo_stack.pop()
            elif char == "M+":
                self.memory += float(self.expression) if self.expression else 0
            elif char == "M-":
                self.memory -= float(self.expression) if self.expression else 0
            elif char == "MRC":
                self.expression = str(self.memory)
            elif char == "MC":
                self.memory = 0
            elif char == "Exit":
                self.root.quit()
            else:
                self.undo_stack.append(self.expression)
                self.expression += char
            self.input_var.set(self.expression)
        except Exception:
            messagebox.showerror("Error", "Invalid Input")
            self.expression = ""
            self.input_var.set("")

    def on_key_press(self, event):
        key = event.char
        if key.isdigit() or key in "+-*/.":
            self.on_button_click(key)
        elif key == "\r":
            self.on_button_click("=")
        elif key == "\x08":
            self.on_button_click("⌫")

    def show_history(self):
        history_window = tk.Toplevel(self.root)
        history_window.title("Calculation History")
        history_window.geometry("400x300")

        # Apply current theme to history window
        bg_color = self.current_theme["bg"]
        fg_color = self.current_theme["fg"]
        
        history_window.configure(bg=bg_color)
        history_listbox = tk.Listbox(history_window, font=("Arial", 12), width=50, height=15,
                                   bg=bg_color, fg=fg_color, selectbackground="#636e72")
        history_listbox.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        for calc in self.history:
            history_listbox.insert(tk.END, calc)

    def save_history_as_pdf(self):
        if not self.history:
            messagebox.showinfo("Info", "No history to save.")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save History as PDF"
        )
        
        if file_path:
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=14)
                pdf.cell(200, 10, "Calculation History", ln=True, align="C")
                
                for calc in self.history:
                    pdf.cell(200, 10, calc, ln=True)
                
                pdf.output(file_path)
                messagebox.showinfo("Success", f"History saved as PDF at:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save PDF:\n{str(e)}")

    def change_theme(self):
        color = colorchooser.askcolor(title="Choose Theme Color")[1]
        if color:
            self.current_theme["bg"] = color
            self.current_theme["fg"] = "#ffffff" if color < "#808080" else "#000000"
            self.current_theme["btn_bg"] = color
            self.current_theme["btn_fg"] = "#ffffff" if color < "#808080" else "#000000"
            self.current_theme["entry_bg"] = color
            self.current_theme["entry_fg"] = "#ffffff" if color < "#808080" else "#000000"
            self.apply_theme()

    def apply_theme(self):
        self.root.configure(bg=self.current_theme["bg"])
        self.entry.configure(bg=self.current_theme["entry_bg"], fg=self.current_theme["entry_fg"])
        self.menu_button.configure(bg=self.current_theme["btn_bg"], fg=self.current_theme["btn_fg"])
        for btn in self.buttons.values():
            btn.configure(bg=self.current_theme["btn_bg"], fg=self.current_theme["btn_fg"])

if __name__ == "__main__":
    root = tk.Tk()
    calculator = ProfessionalCalculator(root)
    root.mainloop()