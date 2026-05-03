"""
Анализатор данных о браках и разводах (Вариант 7).
Наследует от BaseAnalyzer (принципы ООП: наследование, полиморфизм).
"""

from typing import Dict, Any, List
from base_analyzer import BaseAnalyzer


class MarriageAnalyzer(BaseAnalyzer):
    """
    Анализатор данных о браках и разводах в России.
    Вариант 7.
    """
    
    def __init__(self, n_value: int = 5):
        super().__init__(n_value)
        self._years: List[int] = []
        self._marriages: List[int] = []
        self._divorces: List[int] = []
        self._marriage_age_male: List[float] = []
        self._marriage_age_female: List[float] = []
        self._divorce_age_male: List[float] = []
        self._divorce_age_female: List[float] = []
    
    def _validate_data(self) -> None:
        """Валидация данных о браках и разводах."""
        super()._validate_data()
        
        required_fields = ['year', 'marriages', 'divorces']
        for record in self._data:
            for field in required_fields:
                if field not in record:
                    raise ValueError(f"Отсутствует поле '{field}' в данных")
    
    def analyze(self) -> Dict[str, Any]:
        """Анализ данных о браках и разводах."""
        if not self._data:
            return {}
        
        self._years = [record['year'] for record in self._data]
        self._marriages = [int(record['marriages']) for record in self._data]
        self._divorces = [int(record['divorces']) for record in self._data]
        
        self._marriage_age_male = [
            float(record.get('avg_marriage_age_male', 0)) for record in self._data
        ]
        self._marriage_age_female = [
            float(record.get('avg_marriage_age_female', 0)) for record in self._data
        ]
        self._divorce_age_male = [
            float(record.get('avg_divorce_age_male', 0)) for record in self._data
        ]
        self._divorce_age_female = [
            float(record.get('avg_divorce_age_female', 0)) for record in self._data
        ]
        
        results: Dict[str, Any] = {}
        
        if any(self._marriage_age_male):
            max_idx_m = self._marriage_age_male.index(max(self._marriage_age_male))
            min_idx_m = self._marriage_age_male.index(min(self._marriage_age_male))
            results["Мужчины женились позже всего"] = f"{max(self._marriage_age_male)} лет ({self._years[max_idx_m]} г.)"
            results["Мужчины женились раньше всего"] = f"{min(self._marriage_age_male)} лет ({self._years[min_idx_m]} г.)"
        
        if any(self._marriage_age_female):
            max_idx_f = self._marriage_age_female.index(max(self._marriage_age_female))
            min_idx_f = self._marriage_age_female.index(min(self._marriage_age_female))
            results["Женщины выходили замуж позже всего"] = f"{max(self._marriage_age_female)} лет ({self._years[max_idx_f]} г.)"
            results["Женщины выходили замуж раньше всего"] = f"{min(self._marriage_age_female)} лет ({self._years[min_idx_f]} г.)"
        
        if any(self._divorce_age_male):
            max_idx_dm = self._divorce_age_male.index(max(self._divorce_age_male))
            min_idx_dm = self._divorce_age_male.index(min(self._divorce_age_male))
            results["Мужчины разводились позже всего"] = f"{max(self._divorce_age_male)} лет ({self._years[max_idx_dm]} г.)"
            results["Мужчины разводились раньше всего"] = f"{min(self._divorce_age_male)} лет ({self._years[min_idx_dm]} г.)"
        
        if any(self._divorce_age_female):
            max_idx_df = self._divorce_age_female.index(max(self._divorce_age_female))
            min_idx_df = self._divorce_age_female.index(min(self._divorce_age_female))
            results["Женщины разводились позже всего"] = f"{max(self._divorce_age_female)} лет ({self._years[max_idx_df]} г.)"
            results["Женщины разводились раньше всего"] = f"{min(self._divorce_age_female)} лет ({self._years[min_idx_df]} г.)"
        
        results["Всего браков за период"] = f"{sum(self._marriages):,}"
        results["Всего разводов за период"] = f"{sum(self._divorces):,}"
        results["Период"] = f"{self._years[0]} - {self._years[-1]}"
        
        return results
    
    def get_table_data(self) -> List[List[Any]]:
        """Получение данных для таблицы."""
        if not self._data:
            return [["Нет данных"]]
        
        if not self._years:
            self.analyze()
        
        headers = ["Год", "Браки", "Разводы", "Возраст брака М", "Возраст брака Ж"]
        
        rows: List[List[Any]] = []
        for i, year in enumerate(self._years):
            rows.append([
                year,
                f"{self._marriages[i]:,}",
                f"{self._divorces[i]:,}",
                f"{self._marriage_age_male[i]:.1f}" if self._marriage_age_male[i] else "-",
                f"{self._marriage_age_female[i]:.1f}" if self._marriage_age_female[i] else "-"
            ])
        
        return [headers] + rows
    
    def get_chart_data(self) -> Dict[str, Any]:
        """Получение данных для графика."""
        if not self._years:
            self.analyze()
        
        return {
            "years": self._years,
            "values": {
                "Браки (тыс.)": [m / 1000 for m in self._marriages],
                "Разводы (тыс.)": [d / 1000 for d in self._divorces]
            },
            "title": "Браки и разводы в России",
            "ylabel": "Количество (тыс.)"
        }
    
    def get_age_chart_data(self) -> Dict[str, Any]:
        """
        Получение данных для графика возрастов.
        
        Returns:
            Словарь с данными для matplotlib
        """
        if not self._years:
            self.analyze()
        
        return {
            "years": self._years,
            "values": {
                "Возраст брака (мужчины)": self._marriage_age_male,
                "Возраст брака (женщины)": self._marriage_age_female,
                "Возраст развода (мужчины)": self._divorce_age_male,
                "Возраст развода (женщины)": self._divorce_age_female
            },
            "title": "Средний возраст вступления в брак и развода",
            "ylabel": "Возраст (лет)"
        }
    
    def get_variant_info(self) -> str:
        """Информация о варианте задания."""
        return (
            "Вариант 7: Анализ браков и разводов\n\n"
            "Задание:\n"
            "- Открыть файл с данными о браках и разводах за последние 15 лет\n"
            "- Вывести информацию в табличном формате\n"
            "- Построить графики зависимости от года\n"
            "- Вычислить в каком возрасте мужчины и женщины чаще женились и разводились\n"
            "- Реализовать прогнозирование методом скользящей средней"
        )