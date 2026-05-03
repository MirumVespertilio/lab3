"""
Базовый абстрактный класс для анализаторов данных.
Реализует принципы ООП: абстракция, инкапсуляция.
Принципы SOLID: SRP (одна ответственность), OCP (открыт для расширения).
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import json
import os


class BaseAnalyzer(ABC):
    """
    Абстрактный базовый класс для анализа статистических данных.
    
    Атрибуты:
        _data (List[Dict]): Приватный список данных (инкапсуляция)
        _n_value (int): Период для скользящей средней
        _predictions (List[Dict]): Результаты прогнозирования
    """
    
    def __init__(self, n_value: int = 5):
        self._data: List[Dict[str, Any]] = []
        self._n_value = n_value
        self._predictions: List[Dict[str, Any]] = []
    
    @property
    def data(self) -> List[Dict[str, Any]]:
        """Геттер для данных (инкапсуляция)."""
        return self._data
    
    @property
    def predictions(self) -> List[Dict[str, Any]]:
        """Геттер для прогнозов."""
        return self._predictions
    
    @property
    def n_value(self) -> int:
        """Геттер для периода скользящей средней."""
        return self._n_value
    
    @n_value.setter
    def n_value(self, value: int) -> None:
        """Сеттер для периода скользящей средней."""
        if value < 2:
            raise ValueError("Период скользящей средней должен быть >= 2")
        self._n_value = value
    
    def load_data(self, file_path: str) -> bool:
        """Загрузка данных из JSON файла."""
        try:
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"Файл не найден: {file_path}")
            
            with open(file_path, 'r', encoding='utf-8') as f:
                self._data = json.load(f)
            
            self._validate_data()
            return True
            
        except json.JSONDecodeError as e:
            print(f"Ошибка парсинга JSON: {e}")
            return False
        except Exception as e:
            print(f"Ошибка загрузки данных: {e}")
            return False
    
    def _validate_data(self) -> None:
        """Валидация загруженных данных."""
        if not self._data:
            raise ValueError("Данные пусты")
        if not isinstance(self._data, list):
            raise ValueError("Данные должны быть списком")
    
    def moving_average(self, values: List[float], n: Optional[int] = None) -> List[float]:
        """Расчёт скользящей средней."""
        period: int = n if n is not None else self._n_value
        if len(values) < period:
            return []
        
        result: List[float] = []
        for i in range(len(values) - period + 1):
            window = values[i:i + period]
            avg = sum(window) / period
            result.append(avg)
        return result
    
    def extrapolate(self, values: List[float], periods_ahead: int = 3) -> List[float]:
        """Экстраполяция методом скользящей средней."""
        if len(values) < self._n_value:
            return []
        
        extended_values: List[float] = values.copy()
        predictions: List[float] = []
        
        for _ in range(periods_ahead):
            last_n = extended_values[-self._n_value:]
            next_value = sum(last_n) / len(last_n)
            predictions.append(next_value)
            extended_values.append(next_value)
        
        return predictions
    
    def calculate_percentage_change(self, values: List[float]) -> List[Optional[float]]:
        """Расчёт процентного изменения между соседними значениями."""
        if len(values) < 2:
            return []
        
        changes: List[Optional[float]] = [None]
        for i in range(1, len(values)):
            if values[i - 1] != 0:
                change = ((values[i] - values[i - 1]) / values[i - 1]) * 100
                changes.append(round(change, 2))
            else:
                changes.append(None)
        return changes
    
    @abstractmethod
    def analyze(self) -> Dict[str, Any]:
        """Абстрактный метод анализа данных."""
        pass
    
    @abstractmethod
    def get_table_data(self) -> List[List[Any]]:
        """Абстрактный метод получения данных для таблицы."""
        pass
    
    @abstractmethod
    def get_chart_data(self) -> Dict[str, Any]:
        """Абстрактный метод получения данных для графика."""
        pass
    
    @abstractmethod
    def get_variant_info(self) -> str:
        """Информация о варианте задания."""
        pass