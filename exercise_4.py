import tkinter as tk
import random

class HanoiTowers:
    def __init__(self, root):
        self.root = root
        self.root.title("Ханойские башни - Захарова")
        self.root.geometry("1000x600")
        
        #Количество дисков на шпинделях 8..1 (из ID 70200344)
        self.disks_count = [7, 0, 2, 0, 0, 3, 4, 4]  # для шпинделей 8,7,6,5,4,3,2,1
        
        #Начальное состояние
        self.spindles = {i: [] for i in range(1, 9)}
        
        # Заполняем диски (шпиндели от 8 до 1)
        for idx, spindle in enumerate(range(8, 0, -1)):  # 8,7,6,5,4,3,2,1
            cnt = self.disks_count[idx]
            for n in range(1, cnt + 1):
                diameter = spindle * 10 + n
                self.spindles[spindle].append(diameter)
        
        #араметры отрисовки
        self.canvas_width = 950
        self.canvas_height = 450
        #Координаты X для шпинделей 8..1 (слева направо)
        self.spindle_x = [80 + i * 105 for i in range(8)]  # i=0 -> шпиндель 8
        self.disk_height = 18
        self.spindle_base_y = self.canvas_height - 60
        
        #Генерируем цвета для дисков
        self.disk_colors = self.generate_colors()
        self.total_disks = sum(self.disks_count)
        
        self.create_widgets()
        self.draw_towers(self.spindles, 0)
    
    def generate_colors(self):
        colors = {}
        all_disks = []
        for spindle in range(1, 9):
            all_disks.extend(self.spindles[spindle])
        for diam in all_disks:
            r = random.randint(100, 255)
            g = random.randint(100, 255)
            b = random.randint(100, 255)
            colors[diam] = f"#{r:02x}{g:02x}{b:02x}"
        return colors
    
    def create_widgets(self):
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack(pady=10)
        
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        
        # Кнопка НАЧАЛО (слева)
        tk.Button(control_frame, text="Начало", command=self.show_start).pack(side=tk.LEFT, padx=5)
        
        # 4 поля с процентами и кнопками под ними
        self.percent_entries = []
        default_percents = [70, 20, 3, 44]
        
        for i, p in enumerate(default_percents):
            block = tk.Frame(control_frame, relief=tk.RIDGE, bd=1, padx=5, pady=5)
            block.pack(side=tk.LEFT, padx=5)
            entry = tk.Entry(block, width=5)
            entry.insert(0, str(p))
            entry.pack()
            btn = tk.Button(block, text=f"п.{i+1}", 
                           command=lambda e=entry: self.show_percent(e))
            btn.pack(pady=(5, 0))
            self.percent_entries.append(entry)
        
        # Кнопка ОКОНЧАНИЕ (справа)
        tk.Button(control_frame, text="Окончание", command=self.show_end).pack(side=tk.LEFT, padx=5)
        
        self.status_label = tk.Label(self.root, text="Итерация 0", font=("Arial", 12, "bold"), fg="blue")
        self.status_label.pack(pady=10)
    
    def draw_towers(self, state, iteration):
        self.canvas.delete("all")
        
        self.canvas.create_rectangle(40, self.spindle_base_y, self.canvas_width-40, 
                                      self.spindle_base_y + 8, fill="gray", outline="black")
        
        # шпиндели 8..1 слева направо
        for i, x in enumerate(self.spindle_x):
            spindle_num = 8 - i  # i=0 -> 8, i=1 -> 7, ..., i=7 -> 1
            

            self.canvas.create_line(x, self.spindle_base_y - 5, x, self.spindle_base_y - 350, 
                                    width=3, fill="black")

            self.canvas.create_text(x, self.spindle_base_y - 370, text=str(spindle_num), 
                                    font=("Arial", 12, "bold"))
            
            # Диски
            disks = state.get(spindle_num, [])
            for idx, diam in enumerate(disks):
                y = self.spindle_base_y - 5 - (idx + 1) * self.disk_height
                width = diam * 2 + 30
                x1 = x - width // 2
                x2 = x + width // 2
                color = self.disk_colors.get(diam, "lightblue")
                self.canvas.create_rectangle(x1, y, x2, y + self.disk_height, 
                                              fill=color, outline="black", width=1)
                self.canvas.create_text(x, y + self.disk_height // 2, 
                                        text=str(diam), font=("Arial", 8))
        
        self.status_label.config(text=f"Итерация {iteration}")
    
    def show_start(self):
        self.draw_towers(self.spindles, 0)
    
    def show_end(self):
        all_disks = []
        for spindle in range(1, 9):
            all_disks.extend(self.spindles[spindle])
        all_disks.sort(reverse=True)
        end_state = {1: all_disks}
        for i in range(2, 9):
            end_state[i] = []
        self.draw_towers(end_state, self.total_disks * 2)
    
    def show_percent(self, entry):
        try:
            percent = float(entry.get())
            if percent < 0:
                percent = 0
            if percent > 100:
                percent = 100
            
            target_iter = int(percent / 100 * self.total_disks * 2)
            
            demo_state = {i: [] for i in range(1, 9)}
            all_disks = []
            for spindle in range(1, 9):
                all_disks.extend(self.spindles[spindle])
            all_disks.sort(reverse=True)
            
            num_on_1 = int(len(all_disks) * percent / 100)
            demo_state[1] = all_disks[:num_on_1]
            remaining = all_disks[num_on_1:]
            if remaining:
                demo_state[8] = remaining
            
            self.draw_towers(demo_state, target_iter)
        except:
            self.status_label.config(text="Ошибка: введите число")

if __name__ == "__main__":
    root = tk.Tk()
    app = HanoiTowers(root)
    root.mainloop()