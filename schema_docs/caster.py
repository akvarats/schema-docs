from typing import Optional, List, Union

import decimal
import uuid
import datetime


from schema_docs.i import ISchemaDocCaster, ISchemaDoc
from schema_docs.exceptions import SchemaDocFieldException
from schema_docs.utils import field_def_param, safe_iso_to_date, date_to_iso, safe_iso_to_datetime, datetime_to_iso, \
    iso_to_date, iso_to_datetime,  safe_str_to_uuid, uuid_to_str, to_uuid


class SchemaDocCaster(ISchemaDocCaster):

    def __init__(self):
        self.MAP_FROM_EXT = {
            'string': self._from_ext_string,
            'str': self._from_ext_string,
            'number': self._from_ext_number,
            'num': self._from_ext_number,
            'int': self._from_ext_number,
            'array': self._from_ext_list,
            'list': self._from_ext_list,
            'object': self._from_ext_object,
            'obj': self._from_ext_object,
            'date': self._from_ext_date,
            'datetime': self._from_ext_datetime,
            'uuid': self._from_ext_uuid,
            'boolean': self._from_ext_boolean,
            'bool': self._from_ext_boolean
        }

        self.MAP_TO_EXT = {
            'string': self._to_ext_raw,
            'str': self._to_ext_raw,
            'number': self._to_ext_raw,
            'num': self._to_ext_raw,
            'int': self._to_ext_raw,
            'object': self._to_ext_raw,
            'obj': self._to_ext_raw,
            'array': self._to_ext_raw,
            'list': self._to_ext_raw,
            'date': self._to_ext_date,
            'datetime': self._to_ext_datetime,
            'uuid': self._to_ext_uuid,
            'boolean': self._to_ext_raw,
            'bool': self._to_ext_raw
        }

    def from_ext(self, value, field_name: str, field_def: dict, doc: ISchemaDoc):
        """
        Преобразует значение из
        """
        if value is None:
            # Значение None преобразовывать не нужно. Просто отдаем как есть
            return None

        field_type = self._field_type(field_def)

        if field_type in self.MAP_FROM_EXT:
            return self.MAP_FROM_EXT[field_type](value, field_name, field_def, doc)

        elif field_type in doc.ns.types:
            return self._from_ext_sub_doc(value, field_name, field_def, doc)

        else:
            self._raise_not_implemented(value, field_name, field_def)

    def to_ext(self, value, field_name: str, field_def: dict, doc: ISchemaDoc):
        """ """
        field_type = self._field_type(field_def)
        if field_type in self.MAP_TO_EXT:
            return self.MAP_TO_EXT[field_type](value, field_name, field_def, doc)

        elif field_type in doc.ns.types:
            return self._to_ext_sub_doc(value, field_name, field_def, doc)

        self._raise_not_implemented(value, field_name, field_def)

    # ------------------------------------------------------------------------------------------------------------------
    # Методы преобразования значений из внешнего типа
    # ------------------------------------------------------------------------------------------------------------------
    def _from_ext_string(self, value, field_name: str, field_def: dict, doc: ISchemaDoc) -> Optional[str]:
        self._check_value_type(value, field_name, field_def, (str,))
        return value

    def _from_ext_number(self, value, field_name: str, field_def: dict, doc: ISchemaDoc) -> Optional[Union[int, float]]:
        """

        :param value:
        :param field_name:
        :param field_def:
        :param doc:
        :return:
        """
        self._check_value_type(value, field_name, field_def, (int, float, decimal.Decimal))

        if isinstance(value, decimal.Decimal):
            return int(value) if value % 1 == 0 else float(value)

        return value

    def _from_ext_date(self, value, field_name: str, field_def: dict, doc: ISchemaDoc) -> Optional[str]:
        self._check_value_type(value, field_name, field_def, (datetime.date, datetime.datetime, str))

        if isinstance(value, str):
            if safe_iso_to_date(value) is None:
                self._raise_type_error(value, field_name, field_def)
            return value

        return date_to_iso(value.date() if isinstance(value, datetime.datetime) else value)

    def _from_ext_datetime(self, value, field_name: str, field_def: dict, doc: ISchemaDoc) -> Optional[str]:
        self._check_value_type(value, field_name, field_def, (datetime.datetime, str))

        if isinstance(value, str):
            if safe_iso_to_datetime(value) is None:
                self._raise_type_error(value, field_name, field_def)
            return value

        return datetime_to_iso(value)

    def _from_ext_uuid(self, value, field_name: str, field_def: dict, doc: ISchemaDoc) -> Optional[str]:
        self._check_value_type(value, field_name, field_def, (uuid.UUID, str, ))

        if isinstance(value, str):
            if safe_str_to_uuid(value) is None:
                # указали строку, которая не является валидной записью UUID
                self._raise_type_error(value, field_name, field_def)
            return value
        elif value is None:
            return None
        return uuid_to_str(value)

    def _from_ext_list(self, value, field_name, field_def, doc: ISchemaDoc) -> Optional[list]:
        """

        :param value:
        :param field_name:
        :param field_def:
        :param doc:
        :return:
        """
        self._check_value_type(value, field_name, field_def, (list, ))

        # тут надо ещё проверить, что внутри списка находятся объекты нужного типа
        return value

    def _from_ext_object(self, value, field_name: str, field_def: dict, doc: ISchemaDoc) -> Optional[dict]:
        self._check_value_type(value, field_name, field_def, (dict, ISchemaDoc))

        return value.to_dict() if isinstance(value, ISchemaDoc) else value

    def _from_ext_sub_doc(self, value, field_name: str, field_def: dict, doc: ISchemaDoc) -> Optional[dict]:
        self._check_value_type(value, field_name, field_def, (dict, ISchemaDoc))

        return value.to_dict() if isinstance(value, ISchemaDoc) else \
            getattr(doc.ns, field_def_param(field_def, 'type'))(**value).to_dict()

    def _from_ext_boolean(self, value, field_name: str, field_def: dict, doc: ISchemaDoc) -> Optional[bool]:
        self._check_value_type(value, field_name, field_def, (bool, str))

        if value is None:
            return None

        return value in ['true', 'True', '1', 'on', True]

    # ------------------------------------------------------------------------------------------------------------------
    # Методы преобразования к внешнему типу
    # ------------------------------------------------------------------------------------------------------------------
    def _to_ext_raw(self, value, field_name: str, field_def: str, doc: ISchemaDoc):
        return value

    def _to_ext_sub_doc(self, value, field_name: str, field_def: dict, doc: ISchemaDoc):
        if value is None:
            return None
        doc_cls = doc.ns.types[self._field_type(field_def)]
        return doc_cls(value)

    def _to_ext_date(self, value, field_name: str, field_def: dict, doc: ISchemaDoc) -> Optional[datetime.date]:
        return iso_to_date(value) if isinstance(value, str) else None

    def _to_ext_datetime(self, value, field_name: str, field_def: dict, doc: ISchemaDoc):
        return iso_to_datetime(value) if isinstance(value, str) else None

    def _to_ext_uuid(self, value, field_name: str, field_def: dict, doc: ISchemaDoc):
        return to_uuid(value)

    # ------------------------------------------------------------------------------------------------------------------
    # Вспомогательные методы
    # ------------------------------------------------------------------------------------------------------------------
    def _check_value_type(self, value, field_name: str, field_def: dict, available_types: tuple):
        if value is not None and not isinstance(value, available_types):
            self._raise_type_error(value, field_name, field_def)

    def _raise_type_error(self, value, field_name: str, field_def: dict):
        raise SchemaDocFieldException(
            msg='Value {0} is not compatible with field {1} of type {2}'.format(
                value, field_name, self._field_type(field_def)
            ),
            field_name=field_name,
            field_type=self._field_type(field_def),
            failed_value=value
        )

    def _raise_not_implemented(self, value, field_name: str, field_def: dict):
        raise NotImplementedError('Field {0} with type {1} if not implemented for value {2}'.format(
            field_name, self._field_type(field_def), value
        ))

    def _field_type(self, field_def):
        return field_def if isinstance(field_def, str) else field_def['type']
