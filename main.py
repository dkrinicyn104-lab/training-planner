import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

class TrainingPlanner:
    def __init__(self, root):
        # Инициализация основного окна и списка тренировок
        self.root = root
        self.root.title("Training Planner")
        self.trainings = []
        self.load_data()
        self.create_widgets()

    def create_widgets(self):
        """Создание интерфейса приложения"""
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
        tk.Button(self.root, text="Добавить тренировку", command=self.add_training).grid(row=3, column=0, columnspan=2, pady=10
