import datetime
import pytest
import requests
from sqlalchemy import select
from schemas import RubCurrencyExchangeRate
from crud import get_exchange_rate_from_db, get_exchange_rate_from_api, create_exchange_rate
from config import session, CURRENCY_API_KEY
from models import RubCurrencyExchangeRateModel


def test_get_exchange_rate_from_db():
    date = datetime.date.today()
    expected = session.execute(
        select(RubCurrencyExchangeRateModel).where(RubCurrencyExchangeRateModel.date == date)).scalar()
    data = get_exchange_rate_from_db(date=date,
                                     session=session)
    assert data == expected


@pytest.fixture()
def exchange_rate(request):
    date = request.param
    params = {'base': 'RUB',
              'symbols': 'EUR, USD'}
    resp = requests.get(f'https://api.apilayer.com/exchangerates_data/{date}',
                        params=params,
                        headers={
                            "apikey": CURRENCY_API_KEY
                        })
    return RubCurrencyExchangeRate(date=date,
                                   eur=round(1 / resp.json()['rates']['EUR'], 2),
                                   usd=round(1 / resp.json()['rates']['USD'], 2))


@pytest.mark.parametrize('exchange_rate', [datetime.date.today()], indirect=True)
def test_exchange_rate_from_api(exchange_rate):
    date = datetime.date.today()
    result = get_exchange_rate_from_api(date=date)
    assert result == exchange_rate


@pytest.mark.parametrize('exchange_rate', [datetime.date(year=2019, month=1, day=1)], indirect=True)
def test_create_exchange_rate(exchange_rate):
    date = datetime.date(year=2019,
                         month=1,
                         day=1)
    result = create_exchange_rate(date=date,
                                  session=session)
    assert exchange_rate == result

    saved_exchange_rate = session.execute(
        select(RubCurrencyExchangeRateModel).where(RubCurrencyExchangeRateModel.date == date)).scalar()

    assert saved_exchange_rate.date == exchange_rate.date
    assert saved_exchange_rate.eur == exchange_rate.eur
    assert saved_exchange_rate.usd == exchange_rate.usd
