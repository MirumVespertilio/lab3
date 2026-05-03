"""
Главное окно приложения.
Лабораторная работа №3 - Системы контроля версий.
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from typing import Optional, List, Any
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
import json
import os

# Импорт анализаторов
from base_analyzer import BaseAnalyzer
from expenses_analyzer import ExpensesAnalyzer
from marriage_analyzer import MarriageAnalyzer


class StatisticsApp(ctk.CTk):
    """Главное приложение для анализа статистических данных."""
    
    def __init__(self):
        super().__init__()
        
        self.title("Анализ статистических данных - Лабораторная №3")
        self.geometry("1200x800")
        self.minsize(900, 600)
        
        self.current_analyzer: Optional[BaseAnalyzer] = None
        self.data_file_path: Optional[str] = None
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self._create_widgets()
    
    def _create_widgets(self) -> None:
        """Создание всех виджетов интерфейса."""
        
        # === Верхняя панель ===
        self.top_frame = ctk.CTkFrame(self, height=60)
        self.top_frame.pack(fill="x", padx=10, pady=10)
        
        self.btn_open = ctk.CTkButton(
            self.top_frame,
            text="Открыть файл",
            command=self._open_file,
            width=150
        )
        self.btn_open.pack(side="left", padx=10, pady=10)
        
        self.lbl_file = ctk.CTkLabel(
            self.top_frame,
            text="Файл не выбран",
            font=("Arial", 12)
        )
        self.lbl_file.pack(side="left", padx=10, pady=10)
        
        self.lbl_variant = ctk.CTkLabel(
            self.top_frame,
            text="",
            font=("Arial", 12, "bold"),
            text_color="#00ff00"
        )
        self.lbl_variant.pack(side="right", padx=10, pady=10)
        
        # === Левая панель ===
        self.left_frame = ctk.CTkFrame(self, width=250)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=5)
        
        ctk.CTkLabel(
            self.left_frame,
            text="Настройки",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        ctk.CTkLabel(
            self.left_frame,
            text="Период скользящей средней:",
            font=("Arial", 11)
        ).pack(pady=(20, 5))
        
        self.spin_n_value = ctk.CTkEntry(self.left_frame, width=100, placeholder_text="5")
        self.spin_n_value.insert(0, "5")
        self.spin_n_value.pack(pady=5)
        
        ctk.CTkLabel(
            self.left_frame,
            text="Прогноз на (лет):",
            font=("Arial", 11)
        ).pack(pady=(20, 5))
        
        self.spin_forecast = ctk.CTkEntry(self.left_frame, width=100, placeholder_text="3")
        self.spin_forecast.insert(0, "3")
        self.spin_forecast.pack(pady=5)
        
        self.btn_analyze = ctk.CTkButton(
            self.left_frame,
            text="Анализировать",
            command=self._analyze_data,
            state="disabled"
        )
        self.btn_analyze.pack(pady=10, fill="x", padx=20)
        
        self.btn_chart = ctk.CTkButton(
            self.left_frame,
            text="Построить график",
            command=self._show_chart,
            state="disabled"
        )
        self.btn_chart.pack(pady=10, fill="x", padx=20)
        
        self.btn_forecast = ctk.CTkButton(
            self.left_frame,
            text="Прогноз",
            command=self._show_forecast,
            state="disabled"
        )
        self.btn_forecast.pack(pady=10, fill="x", padx=20)
        
        self.btn_export = ctk.CTkButton(
            self.left_frame,
            text="Экспорт графика",
            command=self._export_chart,
            state="disabled"
        )
        self.btn_export.pack(pady=10, fill="x", padx=20)
        
        # === Центральная область ===
        self.center_frame = ctk.CTkFrame(self)
        self.center_frame.pack(side="left", fill="both", expand=True, padx=10, pady=5)
        
        self.lbl_table_title = ctk.CTkLabel(
            self.center_frame,
            text="Данные",
            font=("Arial", 14, "bold")
        )
        self.lbl_table_title.pack(pady=10)
        
        self.table_frame = ctk.CTkScrollableFrame(
            self.center_frame,
            label_text="Таблица данных"
        )
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # === Статус ===
        self.status_frame = ctk.CTkFrame(self, height=30)
        self.status_frame.pack(fill="x", padx=10, pady=5)
        
        self.lbl_status = ctk.CTkLabel(
            self.status_frame,
            text="Готов к работе",
            font=("Arial", 10)
        )
        self.lbl_status.pack(side="left", padx=10, pady=5)
        
        self.canvas: Optional[FigureCanvasTkAgg] = None
        self.current_figure: Optional[Figure] = None
    
    def _open_file(self) -> None:
        """Открытие файла с данными."""
        file_path = filedialog.askopenfilename(
            title="Выберите файл с данными",
            filetypes=[("JSON файлы", "*.json"), ("Все файлы", "*.*")]
        )
        
        if not file_path:
            return
        
        self.data_file_path = file_path
        self.lbl_file.configure(text=os.path.basename(file_path))
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if data and isinstance(data, list):
                first_record = data[0]
                
                if 'consumer_expenses' in first_record:
                    self.current_analyzer = ExpensesAnalyzer()
                    self.lbl_variant.configure(text="Вариант 18: Потребительские расходы")
                elif 'marriages' in first_record or 'divorces' in first_record:
                    self.current_analyzer = MarriageAnalyzer()
                    self.lbl_variant.configure(text="Вариант 7: Браки и разводы")
                else:
                    messagebox.showerror("Ошибка", "Неизвестный формат данных")
                    return
                
                # Проверка на None перед использованием
                if self.current_analyzer is not None:
                    if self.current_analyzer.load_data(file_path):
                        self.btn_analyze.configure(state="normal")
                        self._update_status(f"Загружено записей: {len(self.current_analyzer.data)}")
                    else:
                        messagebox.showerror("Ошибка", "Не удалось загрузить данные")
                    
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при открытии файла:\n{e}")
    
    def _analyze_data(self) -> None:
        """Анализ данных."""
        if self.current_analyzer is None:
            return
        
        try:
            n_val = int(self.spin_n_value.get())
            self.current_analyzer.n_value = n_val
            
            results = self.current_analyzer.analyze()
            self._display_table()
            
            self.btn_chart.configure(state="normal")
            self.btn_forecast.configure(state="normal")
            self.btn_export.configure(state="normal")
            
            self._show_analysis_results(results)
            self._update_status("Анализ завершён")
            
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Неверное значение: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при анализе:\n{e}")
    
    def _display_table(self) -> None:
        """Отображение таблицы."""
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        if self.current_analyzer is None:
            return
        
        table_data = self.current_analyzer.get_table_data()
        headers = table_data[0]
        rows = table_data[1:]
        
        header_frame = ctk.CTkFrame(self.table_frame, fg_color="gray30")
        header_frame.pack(fill="x", pady=(0, 5))
        
        for header in headers:
            lbl = ctk.CTkLabel(
                header_frame,
                text=str(header),
                font=("Arial", 11, "bold"),
                width=15
            )
            lbl.pack(side="left", padx=5, pady=5)
        
        for row_idx, row in enumerate(rows):
            bg_color = "gray20" if row_idx % 2 == 0 else "gray25"
            row_frame = ctk.CTkFrame(self.table_frame, fg_color=bg_color)
            row_frame.pack(fill="x")
            
            for cell in row:
                lbl = ctk.CTkLabel(
                    row_frame,
                    text=str(cell) if cell is not None else "-",
                    font=("Arial", 10),
                    width=15
                )
                lbl.pack(side="left", padx=5, pady=3)
    
    def _show_analysis_results(self, results: dict) -> None:
        """Показ результатов анализа."""
        if not results:
            return
        
        result_window = ctk.CTkToplevel(self)
        result_window.title("Результаты анализа")
        result_window.geometry("500x400")
        
        ctk.CTkLabel(
            result_window,
            text="Результаты анализа",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        text_frame = ctk.CTkScrollableFrame(result_window)
        text_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        for key, value in results.items():
            ctk.CTkLabel(
                text_frame,
                text=f"{key}:",
                font=("Arial", 12, "bold")
            ).pack(anchor="w", padx=10, pady=(10, 0))
            
            ctk.CTkLabel(
                text_frame,
                text=str(value),
                font=("Arial", 11),
                wraplength=450
            ).pack(anchor="w", padx=20)
    
    def _show_chart(self) -> None:
        """Построение графика."""
        if self.current_analyzer is None:
            return
        
        try:
            chart_data = self.current_analyzer.get_chart_data()
            self._draw_chart(chart_data, show_forecast=False)
            self._update_status("График построен")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при построении графика:\n{e}")
    
    def _show_forecast(self) -> None:
        """Построение прогноза."""
        if self.current_analyzer is None:
            return
        
        try:
            forecast_periods = int(self.spin_forecast.get())
            chart_data = self.current_analyzer.get_chart_data()
            self._draw_chart(chart_data, show_forecast=True, forecast_periods=forecast_periods)
            self._update_status("Прогноз построен")
        except ValueError as e:
            messagebox.showerror("Ошибка", f"Неверное значение: {e}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при построении прогноза:\n{e}")
    
    def _draw_chart(self, chart_data: dict, show_forecast: bool = False, forecast_periods: int = 3) -> None:
        """Отрисовка графика."""
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        if self.current_figure:
            plt.close(self.current_figure)
        
        for widget in self.table_frame.winfo_children():
            widget.destroy()
        
        self.current_figure, ax = plt.subplots(figsize=(10, 6))
        plt.style.use('dark_background')
        
        years = chart_data.get('years', [])
        values = chart_data.get('values', {})
        title = chart_data.get('title', 'График')
        ylabel = chart_data.get('ylabel', 'Значение')
        
        colors = ['#00b4d8', '#90be6d', '#f9c74f', '#f8961e', '#f3722c']
        color_idx = 0
        
        for label, vals in values.items():
            ax.plot(years, vals, marker='o', label=label, color=colors[color_idx % len(colors)], linewidth=2)
            color_idx += 1
        
        if show_forecast and len(years) > 0 and self.current_analyzer is not None:
            n_value = self.current_analyzer.n_value
            
            for label, vals in values.items():
                if len(vals) >= n_value:
                    predictions = self.current_analyzer.extrapolate(vals, forecast_periods)
                    
                    if predictions:
                        last_year = years[-1]
                        forecast_years = list(range(last_year + 1, last_year + forecast_periods + 1))
                        
                        all_years = [years[-1]] + forecast_years
                        all_values = [vals[-1]] + predictions
                        
                        ax.plot(all_years, all_values, 
                                marker='s', linestyle='--', 
                                label=f'{label} (прогноз)',
                                alpha=0.7, linewidth=2)
                        
                        ax.axvspan(years[-1] + 0.5, forecast_years[-1] + 0.5, 
                                   alpha=0.1, color='yellow')
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel('Год', fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        self.canvas = FigureCanvasTkAgg(self.current_figure, master=self.table_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        toolbar_frame = ctk.CTkFrame(self.center_frame)
        toolbar_frame.pack(fill="x")
        
        toolbar = NavigationToolbar2Tk(self.canvas, toolbar_frame)
        toolbar.update()
    
    def _export_chart(self) -> None:
        """Экспорт графика."""
        if not self.current_figure:
            messagebox.showwarning("Предупреждение", "Сначала постройте график")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Сохранить график",
            defaultextension=".png",
            filetypes=[
                ("PNG изображение", "*.png"),
                ("PDF документ", "*.pdf"),
                ("JPEG изображение", "*.jpg")
            ]
        )
        
        if file_path:
            self.current_figure.savefig(file_path, dpi=150, bbox_inches='tight', 
                                        facecolor='white', edgecolor='none')
            self._update_status(f"График сохранён: {os.path.basename(file_path)}")
            messagebox.showinfo("Успех", f"График сохранён:\n{file_path}")
    
    def _update_status(self, message: str) -> None:
        """Обновление статуса."""
        self.lbl_status.configure(text=message)


def main() -> None:
    """Точка входа."""
    app = StatisticsApp()
    app.mainloop()


if __name__ == "__main__":
    main()