from typing import Union, Optional

import uuid
import datetime
import dateutil


def field_def_param(field_def: Union[str, dict], param_name: str, default=None):
    """
    Возвращает значение параметра из определения поля в схеме документа

    :param field_def: объект с описанием поля из определения схемы
    :param param_name: наименование параметра
    :param default: значение по умолчанию
    :return:
    """
    result = default

    if isinstance(field_def, str):
        if param_name == 'type':
            # если в определении шага указана только строка - то это тип задачи
            result = field_def
    else:
        result = field_def[param_name] if param_name in field_def else default

    return result


def defaulted_field_def_param(field_def: Union[str, dict], param_name: str):
    """

    :param field_def:
    :param param_name:
    :return:
    """
    return field_def_param(field_def, param_name, default=None)


# ----------------------------------------------------------------------------------------------------------------------
# Касты
# ----------------------------------------------------------------------------------------------------------------------
def iso_to_datetime(iso_datetime: str) -> datetime.datetime:
    return dateutil.parser.parse(iso_datetime)


def iso_to_date(iso_date: str) -> datetime.date:
    return iso_to_datetime(iso_date).date()


def safe_iso_to_date(iso_date: str) -> Optional[datetime.date]:
    try:
        return iso_to_date(iso_date)
    except (TypeError, ValueError):
        return None


def datetime_to_iso(dt: Union[datetime.datetime, datetime.date]) -> str:
    """
    Преобразует дату или дату/время в ISO формат

    :param dt:
    :return:
    """
    return dt.isoformat()


date_to_iso = datetime_to_iso


def safe_iso_to_datetime(iso_datetime: str) -> Optional[datetime.datetime]:
    try:
        return iso_to_datetime(iso_datetime)
    except (TypeError, ValueError):
        return None


# ----------------------------------------------------------------------------------------------------------------------
# UIDS
# ----------------------------------------------------------------------------------------------------------------------
def str_to_uuid(uid: str) -> uuid.UUID:
    return uuid.UUID(uid)


def safe_str_to_uuid(uid: str) -> Optional[uuid.UUID]:
    """
    Выполняет безопасное преобразование строки в токен (в том смысле, что не выбрасывает исключения
    ValueError, TypeError если в uid указано невалидное значение
    :param uid:
    :return:
    """
    try:
        return str_to_uuid(uid)
    except (TypeError, ValueError):
        return None


def to_uuid(value: Union[str, uuid.UUID, None]):
    """
    Преобразование значения value в тип UUID

    :param value:
    :return:
    """

    if isinstance(value, str):
        return str_to_uuid(value)
    elif isinstance(value, uuid.UUID) or value is None:
        return value

    raise NotImplementedError('Преобразование в UUID из {0} не реализовано'.format(type(value)))


def uuid_to_str(uid: uuid.UUID, no_dashes=True) -> str:
    """
    Возвращает UUID в виде строки

    :param uid: значение UUID, которое необходимо преобразовать в строку
    :param no_dashes: убрать тире ('-') в полученном строковом значении
    :return:
    """
    return str(uid).replace('-', '') if no_dashes else str(uid)


ZERO_UUID = uuid.UUID(int=0)


def zero_uuid():
    return ZERO_UUID


def uuid_or_none(value: Optional[uuid.UUID]):
    """
    Возвращает None, если value представляет собой "пустой" uuid
    :param value:
    :return:
    """
    return None if value is None or value == ZERO_UUID else value


ZERO_DATE = datetime.date(year=1, month=1, day=1)
ZERO_DATETIME = datetime.datetime(year=1, month=1, day=1, hour=23, minute=59, second=29)


def is_empty_date(date: datetime.date) -> bool:
    return date <= ZERO_DATE


def is_empty_datetime(datetime: datetime.datetime) -> bool:
    return datetime <= ZERO_DATETIME
