from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import datetime


import numpy as np


from src.utils import get_default_start_date, get_default_end_date, strfdate


@dataclass
class _DateHandler:
    start_date: str = field(default=strfdate(datetime.date.today()), kw_only=True)
    end_date: str = field(default_factory=get_default_end_date, kw_only=True)

    def __post_init__(self):
        self._validate_dates()

    def _validate_dates(self):
        if self.start_date >= self.end_date:
            self.start_date = get_default_start_date(self.end_date)

@dataclass
class TradingStrategy(ABC, _DateHandler):
    """Base asset trading interface"""

    @property
    @abstractmethod
    def managed_returns(self) -> np.ndarray:
        """The logarithmic returns at each time step"""
    
    @property
    @abstractmethod
    def total_managed_return(self) -> float:
        """The total logarithmic returns over time"""

    @property
    @abstractmethod
    def managed_performance(self) -> float:
        """Measure of managed strategy's performance over baseline"""
