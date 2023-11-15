import datetime

from pydantic import BaseModel


class RubCurrencyExchangeRate(BaseModel):
    """
    Модель данных курса обмена рубля
    """
    date: datetime.date
    eur: float
    usd: float
