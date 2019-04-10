from typing import Optional, List

import abc


class ISchemaDocFailedValidation(object, metaclass=abc.ABCMeta):
    """ Описание несработавшего правила валидации документа"""

    @property
    @abc.abstractmethod
    def msg(self) -> str:
        """ Возвращает строку с описанием некорректной валидации """


class ISchemaDoc(object):

    ns = None
    schema = None

    def setup(self, **options):
        """ Настраивает что-то там в документе """

    def from_dict(self, value: dict):
        """ Формирует объект из "чистого" словаря (в котором данные уже содержатся в нужных форматах) """

    def to_dict(self) -> dict:
        """ Возвращает словарь, соответствующий данным документа """

    def validate(self):
        return True

    def failed_validations(self) -> List[ISchemaDocFailedValidation]:
        """ """
        return []


class ISchemaDocNamespace(object, metaclass=abc.ABCMeta):
    """
    Интерфейс области имен для схемных документов
    """
    @property
    @abc.abstractmethod
    def types(self) -> dict:
        """ Возвращает словарь типов из данной области имен """

    @abc.abstractmethod
    def __getattr__(self, item) -> Optional[ISchemaDoc]:
        """ """


class ISchemaDocBuilder(object, metaclass=abc.ABCMeta):
    """
    Интерфейс билдера для schemadoc
    """

    @abc.abstractmethod
    def build_namespace(self, schema: dict) -> ISchemaDocNamespace:
        """ Возвращает построенный объект области имен схемных документов """


class ISchemaDocCaster(object, metaclass=abc.ABCMeta):
    """
    Интерфейс кастера, используемого в схемных документах для перевода значенией из внешнего представления во внутренний
    и обратно
    """

    @abc.abstractmethod
    def from_ext(self, value, field_name: str, field_def: dict, doc: ISchemaDoc):
        """ Преобразование значения из внешнего представления во внутренний """

    @abc.abstractmethod
    def to_ext(self, value, field_name: str, field_def: dict, doc: ISchemaDoc):
        """ Преобразование значения из внутренного представления во внутреннее """

    @property
    @abc.abstractmethod
    def allow_number_as_string(self) -> bool:
        """ Возвращает True, если присваивание числовому полю значения нормального числа, но в строке допустимо """


class ISchemaDocValidator(object, metaclass=abc.ABCMeta):
    """
    Интерфейс валидатора, используемого в схемных документах для проверки данных
    """

    @abc.abstractmethod
    def failed_validation(self, schema_doc: ISchemaDoc) -> List[ISchemaDocFailedValidation]:
        """ Возвращает список """


class ISchemaDocValidationRule(object, metaclass=abc.ABCMeta):
    """
    """

    @abc.abstractmethod
    def validate(self, doc: ISchemaDoc) -> Optional[ISchemaDocFailedValidation]:
        """ """
