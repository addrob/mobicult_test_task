import requests
from config import CURRENCY_API_KEY
from sqlalchemy import select
from sqlalchemy.orm import Session
from models import RubCurrencyExchangeRateModel
from schemas import RubCurrencyExchangeRate
import datetime

BASE_URL = 'https://api.apilayer.com/exchangerates_data'
headers = {
    "apikey": CURRENCY_API_KEY
}


def get_exchange_rate_from_db(date: datetime.date,
                              session: Session):
    """
    Получение курса обмена из базы данных
    :param date: дата
    :param session: сессия базы данных
    :return: курс обмена
    """
    return session.execute(
        select(RubCurrencyExchangeRateModel).where(RubCurrencyExchangeRateModel.date == date)).scalar()


def get_exchange_rate_from_api(date: datetime.date):
    """
    Получение курса обмена из АПИ
    :param date: дата
    :return: курс обмена
    """
    if date == datetime.date.today():
        params = {'symbols': 'EUR, USD',
                  'base': 'RUB'}
        response = requests.get(f'{BASE_URL}/latest',
                                params=params,
                                headers=headers)
        eur_exchange_rate = round(1 / response.json()['rates']['EUR'], 2)
        usd_exchange_rate = round(1 / response.json()['rates']['USD'], 2)

        return RubCurrencyExchangeRate(date=date,
                                       eur=eur_exchange_rate,
                                       usd=usd_exchange_rate)
    params = {'symbols': ['EUR, USD'],
              'base': 'RUB'}
    response = requests.get(f'{BASE_URL}/{date}',
                            params=params,
                            headers=headers)
    eur_exchange_rate = round(1 / response.json()['rates']['EUR'], 2)
    usd_exchange_rate = round(1 / response.json()['rates']['USD'], 2)

    return RubCurrencyExchangeRate(date=date,
                                   eur=eur_exchange_rate,
                                   usd=usd_exchange_rate)


def create_exchange_rate(date: datetime.date,
                         session: Session):
    """
    Получение и сохранение курса обмена в базу данных
    :param date: дата
    :param session: сессия базы данных
    :return: курс обмена
    """
    data = get_exchange_rate_from_api(date=date)
    exchange_rate_model = RubCurrencyExchangeRateModel(date=date,
                                                       eur=data.eur,
                                                       usd=data.usd)
    session.add(exchange_rate_model)
    session.commit()

    return data
