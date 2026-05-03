"""
Анализатор потребительских расходов (Вариант 18).
Наследует от BaseAnalyzer (принципы ООП: наследование, полиморфизм).
"""

from typing import Dict, Any, List, Optional
from base_analyzer import BaseAnalyzer


class ExpensesAnalyzer(BaseAnalyzer):
    """
    Анализатор данных о потребительских расходах населения.
    Вариант 18.
    """
    
    def __init__(self, n_value: int = 5):
        super().__init__(n_value)
        self._years: List[int] = []
        self._expenses: List[float] = []
        self._percent_changes: List[Optional[float]] = []
    
    def _validate_data(self) -> None:
        """Валидация данных о потребительских расходах."""
        super()._validate_data()
        
        for record in self._data:
            if 'year' not in record:
                raise ValueError("Отсутствует поле 'year' в данных")
            if 'consumer_expenses' not in record:
                raise ValueError("Отсутствует поле 'consumer_expenses' в данных")
    
    def analyze(self) -> Dict[str, Any]:
        """Анализ данных о потребительских расходах."""
        if not self._data:
            return {}
        
        self._years = [record['year'] for record in self._data]
        self._expenses = [float(record['consumer_expenses']) for record in self._data]
        
        self._percent_changes = self.calculate_percentage_change(self._expenses)
        
        valid_changes = [(i, ch) for i, ch in enumerate(self._percent_changes) if ch is not None]
        
        if valid_changes:
            max_change = max(valid_changes, key=lambda x: x[1])
            min_change = min(valid_changes, key=lambda x: x[1])
            
            max_year = self._years[max_change[0]]
            min_year = self._years[min_change[0]]
            max_percent = max_change[1]
            min_percent = min_change[1]
        else:
            max_year = min_year = max_percent = min_percent = None
        
        return {
            "Максимальный рост": f"{max_percent}% ({max_year} год)" if max_percent else "Нет данных",
            "Минимальный рост (или падение)": f"{min_percent}% ({min_year} год)" if min_percent else "Нет данных",
            "Всего записей": len(self._data),
            "Период": f"{self._years[0]} - {self._years[-1]}",
            "Средние расходы": f"{sum(self._expenses) / len(self._expenses):.0f} руб./мес."
        }
    
    def get_table_data(self) -> List[List[Any]]:
        """Получение данных для таблицы."""
        if not self._data:
            return [["Нет данных"]]
        
        if not self._years:
            self.analyze()
        
        headers = ["Год", "Расходы (руб.)", "Изменение (%)"]
        
        rows: List[List[Any]] = []
        for i, year in enumerate(self._years):
            change = self._percent_changes[i]
            rows.append([
                year,
                f"{self._expenses[i]:,.0f}",
                f"{change:+.2f}%" if change is not None else "-"
            ])
        
        return [headers] + rows
    
    def get_chart_data(self) -> Dict[str, Any]:
        """Получение данных для графика."""
        if not self._years:
            self.analyze()
        
        return {
            "years": self._years,
            "values": {
                "Потребительские расходы": self._expenses
            },
            "title": "Потребительские расходы населения России",
            "ylabel": "Расходы (руб./мес.)"
        }
    
    def get_variant_info(self) -> str:
        """Информация о варианте задания."""
        return (
            "Вариант 18: Анализ потребительских расходов\n\n"
            "Задание:\n"
            "- Открыть файл с данными о потребительских расходах за последние 15 лет\n"
            "- Вывести информацию в табличном формате\n"
            "- Построить графики зависимости от года\n"
            "- Вычислить максимальный и минимальный процент изменения за год\n"
            "- Реализовать прогнозирование методом скользящей средней"
        )