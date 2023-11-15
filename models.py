from sqlalchemy import Column, Integer, Float, Date
from config import Base


class RubCurrencyExchangeRateModel(Base):
    """
    Модель базы данных курс обмена рубля
    """
    __tablename__ = 'rub_currency_exchange_rates'
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    eur = Column(Float)
    usd = Column(Float)

