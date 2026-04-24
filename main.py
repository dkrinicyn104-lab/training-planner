import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

class TrainingPlanner:
    def __init__(self, root):
        self.root = root
        self.root.title("Training Planner")
        self.trainings = []
        self.load_data()
        self.create_widgets()
        
    def create_widgets(self):
        # Поля ввода
        tk.Label(self.root, text="Дата (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        self.date_entry = tk.Entry(self.root)
        self.date_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(self.root, text="Тип тренировки:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        self.type_entry = tk.Entry(self.root)
        self.type_entry.grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(self.root, text="Длительность (мин):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        self.duration_entry = tk.Entry(self.root)
        self.duration_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Кнопка добавления
        tk.Button(self.root, text="Добавить тренировку", command=self.add_training).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Фильтры
        tk.Label(self.root, text="Фильтр по типу:").grid(row=4, column=0, padx=10, pady=5, sticky="e")
        self.filter_type = tk.Entry(self.root)
        self.filter_type.grid(row=4, column=1, padx=10, pady=5)
        
        tk.Label(self.root, text="Фильтр по дате:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
        self.filter_date = tk.Entry(self.root)
        self.filter_date.grid(row=5, column=1, padx=10, pady=5)
        
        tk.Button(self.root, text="Применить фильтр", command=self.apply_filter).grid(row=6, column=0, columnspan=2, pady=5)
        
        # Таблица
        columns = ('date', 'type', 'duration')
        self.tree = ttk.Treeview(self.root, columns=columns, show='headings')
        self.tree.heading('date', text='Дата')
        self.tree.heading('type', text='Тип тренировки')
        self.tree.heading('duration', text='Длительность')
        self.tree.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
                self.refresh_table()
    
    def validate_input(self, date, duration, training_type):
        # 1. Проверка типа тренировки (не пустой)
        if not training_type or not training_type.strip():
            messagebox.showerror("Ошибка", "Тип тренировки не может быть пустым")
            return False
        
        # 2. Проверка формата даты
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте YYYY-MM-DD")
            return False
        
        # 3. Проверка длительности
        try:
            dur = int(duration)
            if dur <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Длительность должна быть положительным числом")
            return False
        
        return True
    
    def add_training(self):
        date = self.date_entry.get()
        training_type = self.type_entry.get()
        duration = self.duration_entry.get()
        
        if not self.validate_input(date, duration, training_type):
            return
        
        self.trainings.append({
            'date': date, 
            'type': training_type.strip(), 
            'duration': int(duration)
        })
        
        self.save_data()
        self.refresh_table()
        self.clear_inputs()
    
    def apply_filter(self):
        try:
            filter_type = self.filter_type.get().lower().strip()
            filter_date = self.filter_date.get().strip()
            
            # Очищаем таблицу            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Фильтруем данные
            for training in self.trainings:
                type_match = (not filter_type) or (filter_type in training['type'].lower())
                date_match = (not filter_date) or (filter_date == training['date'])
                
                if type_match and date_match:
                    self.tree.insert('', tk.END, values=(training['date'], training['type'], training['duration']))
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при фильтрации: {e}")
    
    def refresh_table(self):
        # Полное обновление таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for training in self.trainings:
            self.tree.insert('', tk.END, values=(training['date'], training['type'], training['duration']))
    
    def clear_inputs(self):
        self.date_entry.delete(0, tk.END)
        self.type_entry.delete(0, tk.END)
        self.duration_entry.delete(0, tk.END)
    
    def save_data(self):
        try:
            with open('trainings.json', 'w', encoding='utf-8') as f:
                json.dump(self.trainings, f, ensure_ascii=False, indent=2)
        except IOError as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")
    
    def load_data(self):
        if os.path.exists('trainings.json'):
            try:
                with open('trainings.json', 'r', encoding='utf-8') as f:
                    self.trainings = json.load(f)
            except json.JSONDecodeError:
                self.trainings = []
            except IOError:
                self.trainings = []

if __name__ == "__main__":
    root = tk.Tk()
    app = TrainingPlanner(root)
    root.mainloop()
