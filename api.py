from typing import Annotated

from fastapi import APIRouter, Path, Request, Depends
import datetime
from fastapi.responses import HTMLResponse
from config import session, currency_client, templates
from crud import get_exchange_rate_from_db, create_exchange_rate

router = APIRouter()


def get_dates():
    """
    Получение словаря ближайших дат
    :return: словарь дать
    """
    return {'today': datetime.date.today(),
            'yesterday': datetime.date.today() - datetime.timedelta(days=1),
            'day_before_yesterday': datetime.date.today() - datetime.timedelta(days=2)}


@router.get('/',
            response_class=HTMLResponse)
def get_index(request: Request,
              dates: dict = Depends(get_dates)):
    """
    Обработка начальной страницы
    :param request: запрос
    :param dates: словарь ближайших дат
    """
    date = datetime.date.today()
    return get_exchange_rate(request=request,
                             date=date,
                             dates=dates)


@router.get('/rub_exchange_rate/{date}',
            response_class=HTMLResponse)
def get_exchange_rate(request: Request,
                      dates: dict = Depends(get_dates),
                      date: datetime.date = Path()):
    """
    Обработка страницы курса валют по дате
    :param request: запрос
    :param dates: словарь ближайщих дат
    :param date: дата
    """
    if get_exchange_rate_from_db(date=date,
                                 session=session) is None:
        exchange_rate = create_exchange_rate(date=date,
                                             session=session)
        return templates.TemplateResponse('index.html',
                                          {'request': request, 'exchange_rate': exchange_rate, 'dates': dates})

    exchange_rate = get_exchange_rate_from_db(date=date,
                                              session=session)
    return templates.TemplateResponse('index.html',
                                      {'request': request, 'exchange_rate': exchange_rate, 'dates': dates})
