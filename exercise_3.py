import tkinter as tk
from tkinter import font
import math

class ModernCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор - Zakharova")
        self.root.geometry("480x650")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e2e")
        
        # Параметры по ID 70200344
        self.display_lines = 4
        self.mem_cells = 2
        self.memory = [0, 0]
        self.current_mem = 0
        self.history = []
        
        # Режимы
        self.simple_mode = True
        self.current_expression = ""
        
        # Цветовая схема
        self.colors = {
            'bg': '#1e1e2e',
            'display_bg': '#2d2d3f',
            'display_fg': '#ffffff',
            'history_fg': '#89b4fa',
            'btn_num': '#313244',
            'btn_num_fg': '#cdd6f4',
            'btn_op': '#89b4fa',
            'btn_op_fg': '#1e1e2e',
            'btn_func': '#f9e2af',
            'btn_func_fg': '#1e1e2e',
            'btn_eq': '#a6e3a1',
            'btn_eq_fg': '#1e1e2e',
            'btn_mem': '#cba6f7',
            'btn_mem_fg': '#1e1e2e',
            'btn_clear': '#f38ba8',
            'btn_clear_fg': '#1e1e2e'
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        # Дисплей
        display_frame = tk.Frame(self.root, bg=self.colors['bg'])
        display_frame.pack(pady=(20, 10), padx=20, fill='both')
        
        # Поле истории
        self.history_text = tk.Text(
            display_frame, 
            height=self.display_lines-1, 
            bg=self.colors['display_bg'],
            fg=self.colors['history_fg'],
            font=('Consolas', 10),
            relief='flat',
            wrap='word'
        )
        self.history_text.pack(fill='both', padx=5, pady=(5, 0))
        self.history_text.config(state=tk.DISABLED)
        
        # Поле ввода
        self.entry_var = tk.StringVar()
        self.entry = tk.Entry(
            display_frame, 
            textvariable=self.entry_var,
            font=('Segoe UI', 20, 'bold'),
            bg=self.colors['display_bg'],
            fg=self.colors['display_fg'],
            relief='flat',
            justify='right',
            insertbackground='white'
        )
        self.entry.pack(fill='both', padx=5, pady=(5, 5))
        
        # Рамка для кнопок
        self.button_frame = tk.Frame(self.root, bg=self.colors['bg'])
        self.button_frame.pack(padx=20, pady=10, fill='both', expand=True)
        
        # Создаём кнопки обычного режима
        self.create_simple_buttons()
        
        # Кнопка переключения режима
        self.mode_btn = tk.Button(
            self.root,
            text="🔬 Инженерный",
            font=('Segoe UI', 10, 'bold'),
            bg=self.colors['btn_func'],
            fg=self.colors['btn_func_fg'],
            relief='flat',
            cursor='hand2',
            command=self.toggle_mode
        )
        self.mode_btn.pack(pady=(0, 10))
        
        # Создаём панель памяти
        self.create_memory_panel()
    
    def create_button(self, parent, text, row, col, color_key, command=None, colspan=1, sticky='nsew'):
        """Создаёт красивую кнопку"""
        btn = tk.Button(
            parent,
            text=text,
            font=('Segoe UI', 12, 'bold'),
            bg=self.colors[color_key],
            fg=self.colors[f'{color_key}_fg'],
            relief='flat',
            cursor='hand2',
            activebackground='#45475a',
            command=command or (lambda t=text: self.click(t))
        )
        btn.grid(row=row, column=col, columnspan=colspan, padx=3, pady=3, sticky=sticky)
        
        # Анимация при наведении
        def on_enter(e):
            btn.config(bg='#45475a')
        def on_leave(e):
            btn.config(bg=self.colors[color_key])
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        return btn
    
    def create_simple_buttons(self):
        # Очищаем фрейм
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        
        # Настройка сетки
        for i in range(5):
            self.button_frame.grid_rowconfigure(i, weight=1)
        for j in range(5):
            self.button_frame.grid_columnconfigure(j, weight=1)
        
        # Кнопки
        buttons = [
            ('7', 0, 0, 'btn_num'), ('8', 0, 1, 'btn_num'), ('9', 0, 2, 'btn_num'),
            ('/', 0, 3, 'btn_op'), ('C', 0, 4, 'btn_clear'),
            
            ('4', 1, 0, 'btn_num'), ('5', 1, 1, 'btn_num'), ('6', 1, 2, 'btn_num'),
            ('*', 1, 3, 'btn_op'), ('√', 1, 4, 'btn_func'),
            
            ('1', 2, 0, 'btn_num'), ('2', 2, 1, 'btn_num'), ('3', 2, 2, 'btn_num'),
            ('-', 2, 3, 'btn_op'), ('±', 2, 4, 'btn_func'),
            
            ('0', 3, 0, 'btn_num'), ('.', 3, 1, 'btn_num'), ('=', 3, 2, 'btn_eq'),
            ('+', 3, 3, 'btn_op'), ('^', 3, 4, 'btn_func')
        ]
        
        for btn in buttons:
            self.create_button(
                self.button_frame, btn[0], btn[1], btn[2], btn[3],
                command=(lambda t=btn[0]: self.click(t)) if btn[0] != '=' else self.calculate
            )
    
    def create_engineering_buttons(self):
        # Очищаем фрейм
        for widget in self.button_frame.winfo_children():
            widget.destroy()
        
        # Настройка сетки (5x6 для инженерных кнопок)
        for i in range(6):
            self.button_frame.grid_rowconfigure(i, weight=1)
        for j in range(6):
            self.button_frame.grid_columnconfigure(j, weight=1)
        
        # Базовые кнопки
        basic_buttons = [
            ('7', 0, 0, 'btn_num'), ('8', 0, 1, 'btn_num'), ('9', 0, 2, 'btn_num'),
            ('/', 0, 3, 'btn_op'), ('C', 0, 4, 'btn_clear'),
            
            ('4', 1, 0, 'btn_num'), ('5', 1, 1, 'btn_num'), ('6', 1, 2, 'btn_num'),
            ('*', 1, 3, 'btn_op'), ('√', 1, 4, 'btn_func'),
            
            ('1', 2, 0, 'btn_num'), ('2', 2, 1, 'btn_num'), ('3', 2, 2, 'btn_num'),
            ('-', 2, 3, 'btn_op'), ('±', 2, 4, 'btn_func'),
            
            ('0', 3, 0, 'btn_num'), ('.', 3, 1, 'btn_num'), ('=', 3, 2, 'btn_eq'),
            ('+', 3, 3, 'btn_op'), ('^', 3, 4, 'btn_func')
        ]
        
        for btn in basic_buttons:
            self.create_button(
                self.button_frame, btn[0], btn[1], btn[2], btn[3],
                command=(lambda t=btn[0]: self.click(t)) if btn[0] != '=' else self.calculate
            )
        
        # Инженерные функции
        eng_buttons = [
            ('arsinh', 0, 5, 'btn_func'), ('exp', 1, 5, 'btn_func'),
            ('asin', 2, 5, 'btn_func'), ('acos', 3, 5, 'btn_func')
        ]
        
        for btn in eng_buttons:
            self.create_button(
                self.button_frame, btn[0], btn[1], btn[2], btn[3],
                command=lambda t=btn[0]: self.special_function(t)
            )
    
    def create_memory_panel(self):
        """Панель памяти внизу"""
        mem_frame = tk.Frame(self.root, bg=self.colors['bg'])
        mem_frame.pack(pady=(0, 10), padx=20, fill='x')
        
        # Кнопки M1, M2
        btn_m1 = tk.Button(
            mem_frame, text="M1", font=('Segoe UI', 10, 'bold'),
            bg=self.colors['btn_mem'], fg=self.colors['btn_mem_fg'],
            relief='flat', cursor='hand2',
            command=lambda: self.recall_memory(0)
        )
        btn_m1.pack(side=tk.LEFT, padx=5, expand=True, fill='x')
        
        btn_m2 = tk.Button(
            mem_frame, text="M2", font=('Segoe UI', 10, 'bold'),
            bg=self.colors['btn_mem'], fg=self.colors['btn_mem_fg'],
            relief='flat', cursor='hand2',
            command=lambda: self.recall_memory(1)
        )
        btn_m2.pack(side=tk.LEFT, padx=5, expand=True, fill='x')
        
        btn_ms = tk.Button(
            mem_frame, text="MS", font=('Segoe UI', 10, 'bold'),
            bg=self.colors['btn_mem'], fg=self.colors['btn_mem_fg'],
            relief='flat', cursor='hand2',
            command=self.memory_store
        )
        btn_ms.pack(side=tk.LEFT, padx=5, expand=True, fill='x')
        
        btn_mr = tk.Button(
            mem_frame, text="MR", font=('Segoe UI', 10, 'bold'),
            bg=self.colors['btn_mem'], fg=self.colors['btn_mem_fg'],
            relief='flat', cursor='hand2',
            command=self.memory_recall
        )
        btn_mr.pack(side=tk.LEFT, padx=5, expand=True, fill='x')
        
        btn_m_plus = tk.Button(
            mem_frame, text="M+", font=('Segoe UI', 10, 'bold'),
            bg=self.colors['btn_mem'], fg=self.colors['btn_mem_fg'],
            relief='flat', cursor='hand2',
            command=self.memory_add
        )
        btn_m_plus.pack(side=tk.LEFT, padx=5, expand=True, fill='x')
        
        btn_m_minus = tk.Button(
            mem_frame, text="M-", font=('Segoe UI', 10, 'bold'),
            bg=self.colors['btn_mem'], fg=self.colors['btn_mem_fg'],
            relief='flat', cursor='hand2',
            command=self.memory_sub
        )
        btn_m_minus.pack(side=tk.LEFT, padx=5, expand=True, fill='x')
        
        btn_mc = tk.Button(
            mem_frame, text="MC", font=('Segoe UI', 10, 'bold'),
            bg=self.colors['btn_mem'], fg=self.colors['btn_mem_fg'],
            relief='flat', cursor='hand2',
            command=self.memory_clear
        )
        btn_mc.pack(side=tk.LEFT, padx=5, expand=True, fill='x')
        
        # Индикатор активной ячейки
        self.mem_indicator = tk.Label(
            mem_frame, text="→ M1", font=('Segoe UI', 9),
            bg=self.colors['bg'], fg=self.colors['btn_mem']
        )
        self.mem_indicator.pack(side=tk.LEFT, padx=10)
        
        # Переключатель ячейки
        btn_switch = tk.Button(
            mem_frame, text="🔄", font=('Segoe UI', 10, 'bold'),
            bg=self.colors['btn_mem'], fg=self.colors['btn_mem_fg'],
            relief='flat', cursor='hand2',
            command=self.switch_memory
        )
        btn_switch.pack(side=tk.LEFT, padx=5)
    
    def switch_memory(self):
        self.current_mem = 1 - self.current_mem
        self.mem_indicator.config(text=f"→ M{self.current_mem + 1}")
    
    def memory_store(self):
        try:
            val = float(self.entry_var.get())
            self.memory[self.current_mem] = val
            self.add_to_history(f"MS → M{self.current_mem+1} = {val}")
        except:
            pass
    
    def memory_recall(self):
        val = self.memory[self.current_mem]
        self.entry_var.set(str(val))
        self.current_expression = str(val)
    
    def recall_memory(self, idx):
        self.entry_var.set(str(self.memory[idx]))
        self.current_expression = str(self.memory[idx])
    
    def memory_add(self):
        try:
            val = float(self.entry_var.get())
            self.memory[self.current_mem] += val
            self.add_to_history(f"M{self.current_mem+1} += {val} → {self.memory[self.current_mem]}")
        except:
            pass
    
    def memory_sub(self):
        try:
            val = float(self.entry_var.get())
            self.memory[self.current_mem] -= val
            self.add_to_history(f"M{self.current_mem+1} -= {val} → {self.memory[self.current_mem]}")
        except:
            pass
    
    def memory_clear(self):
        self.memory[self.current_mem] = 0
        self.add_to_history(f"M{self.current_mem+1} = 0")
    
    def special_function(self, func):
        try:
            val = float(self.entry_var.get() or "0")
            if func == "arsinh":
                result = math.asinh(val)
            elif func == "exp":
                result = math.exp(val)
            elif func == "asin":
                result = math.asin(val) if -1 <= val <= 1 else "Ошибка"
            elif func == "acos":
                result = math.acos(val) if -1 <= val <= 1 else "Ошибка"
            else:
                result = "Ошибка"
            
            self.add_to_history(f"{func}({val}) = {result}")
            self.entry_var.set(str(result))
            self.current_expression = str(result)
        except:
            self.entry_var.set("Ошибка")
    
    def click(self, key):
        if key == 'C':
            self.current_expression = ""
            self.entry_var.set("")
        elif key == '√':
            try:
                val = float(self.current_expression or self.entry_var.get())
                result = math.sqrt(val)
                self.add_to_history(f"√({val}) = {result}")
                self.current_expression = str(result)
                self.entry_var.set(str(result))
            except:
                self.entry_var.set("Ошибка")
        elif key == '±':
            if self.current_expression.startswith('-'):
                self.current_expression = self.current_expression[1:]
            else:
                self.current_expression = '-' + self.current_expression
            self.entry_var.set(self.current_expression)
        elif key == '^':
            self.current_expression += '**'
            self.entry_var.set(self.current_expression)
        else:
            self.current_expression += key
            self.entry_var.set(self.current_expression)
    
    def calculate(self):
        try:
            result = eval(self.current_expression)
            self.add_to_history(f"{self.current_expression} = {result}")
            self.current_expression = str(result)
            self.entry_var.set(str(result))
        except:
            self.entry_var.set("Ошибка")
    
    def add_to_history(self, text):
        self.history.append(text)
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, text + "\n")
        self.history_text.see(tk.END)
        self.history_text.config(state=tk.DISABLED)
    
    def toggle_mode(self):
        self.simple_mode = not self.simple_mode
        if self.simple_mode:
            self.create_simple_buttons()
            self.mode_btn.config(text="Инженерный")
            self.root.geometry("480x650")
        else:
            self.create_engineering_buttons()
            self.mode_btn.config(text="Обычный")
            self.root.geometry("620x650")

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernCalculator(root)
    root.mainloop()