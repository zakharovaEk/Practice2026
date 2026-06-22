import tkinter as tk
from tkinter import scrolledtext, messagebox

class BankSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Банковская система - Zakharova")
        # Счёт на фамилию с суммой = ID
        self.accounts = {"Zakharova": 70200344}
        
        # Интерфейс
        tk.Label(root, text="Команды (по одной на строке):").pack()
        self.cmd_text = scrolledtext.ScrolledText(root, height=10, width=60)
        self.cmd_text.pack(pady=5)
        self.cmd_text.bind("<Return>", lambda e: self.execute())
        
        btn_frame = tk.Frame(root)
        btn_frame.pack()
        tk.Button(btn_frame, text="Расчёт", command=self.execute).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Очистить ввод", command=self.clear_input).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Очистить вывод", command=self.clear_output).pack(side=tk.LEFT, padx=5)
        
        tk.Label(root, text="Результаты:").pack()
        self.out_text = scrolledtext.ScrolledText(root, height=15, width=60)
        self.out_text.pack(pady=5)
        
        tk.Label(root, text="Имя файла:").pack()
        self.file_entry = tk.Entry(root, width=40)
        self.file_entry.pack(pady=5)
        tk.Button(root, text="Загрузить", command=self.load_file).pack()
        
        self.root.bind("<Shift-Return>", lambda e: self.load_file())
    
    def execute(self):
        self.out_text.delete(1.0, tk.END)
        commands = self.cmd_text.get(1.0, tk.END).strip().split("\n")
        
        for cmd_line in commands:
            if not cmd_line.strip():
                continue
            self.out_text.insert(tk.END, f"{cmd_line}\n")
            parts = cmd_line.split()
            if not parts:
                continue
            cmd = parts[0].upper()
            try:
                if cmd == "DEPOSIT":
                    name, sum_ = parts[1], int(parts[2])
                    if name not in self.accounts:
                        self.accounts[name] = 0
                    self.accounts[name] += sum_
                    self.out_text.insert(tk.END, f"    {name} {self.accounts[name]}\n")
                elif cmd == "WITHDRAW":
                    name, sum_ = parts[1], int(parts[2])
                    if name not in self.accounts:
                        self.accounts[name] = 0
                    self.accounts[name] -= sum_
                    self.out_text.insert(tk.END, f"    {name} {self.accounts[name]}\n")
                elif cmd == "BALANCE":
                    if len(parts) == 1:
                        for n, b in self.accounts.items():
                            self.out_text.insert(tk.END, f"    {n} {b}\n")
                    else:
                        name = parts[1]
                        if name in self.accounts:
                            self.out_text.insert(tk.END, f"    {name} {self.accounts[name]}\n")
                        else:
                            self.out_text.insert(tk.END, f"    NO CLIENT\n")
                elif cmd == "TRANSFER":
                    name1, name2, sum_ = parts[1], parts[2], int(parts[3])
                    for n in (name1, name2):
                        if n not in self.accounts:
                            self.accounts[n] = 0
                    self.accounts[name1] -= sum_
                    self.accounts[name2] += sum_
                    self.out_text.insert(tk.END, f"    {name1} {self.accounts[name1]}\n    {name2} {self.accounts[name2]}\n")
                elif cmd == "INCOME":
                    p = int(parts[1])
                    for name in list(self.accounts.keys()):
                        if self.accounts[name] > 0:
                            self.accounts[name] = int(self.accounts[name] * (1 + p / 100))
                    for name, bal in self.accounts.items():
                        self.out_text.insert(tk.END, f"    {name} {bal}\n")
                else:
                    self.out_text.insert(tk.END, f"ОШИБКА: {cmd_line}\n")
                    break
            except Exception:
                self.out_text.insert(tk.END, f"ОШИБКА: {cmd_line}\n")
                break
            self.out_text.insert(tk.END, ">>>\n")
    
    def load_file(self):
        filename = self.file_entry.get().strip()
        if not filename:
            messagebox.showerror("Ошибка", "Введите имя файла")
            return
        try:
            with open(filename, "r", encoding="utf-8") as f:
                self.cmd_text.delete(1.0, tk.END)
                self.cmd_text.insert(1.0, f.read())
        except FileNotFoundError:
            messagebox.showerror("Ошибка", f"Файл {filename} не найден")
    
    def clear_input(self):
        self.cmd_text.delete(1.0, tk.END)
    
    def clear_output(self):
        self.out_text.delete(1.0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = BankSystem(root)
    root.mainloop()