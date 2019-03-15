from typing import Optional, List

from schema_docs.utils import defaulted_field_def_param, field_def_param, zero_uuid, is_empty_date, is_empty_datetime


from schema_docs.i import ISchemaDoc, ISchemaDocFailedValidation, ISchemaDocValidator, ISchemaDocValidationRule


class SchemaDocValidator(ISchemaDocValidator):
    """ Валидатор """

    def failed_validation(self, schema_doc: ISchemaDoc) -> List[ISchemaDocFailedValidation]:

        result = []

        validation_rules = self._collect_validation_rules(schema_doc)
        for rule in validation_rules:
            validation_result = rule.validate(schema_doc)
            if validation_result is not None:
                result.append(validation_result)

        # Если в списке полей есть вложенное значение, то валидируем его тоже
        for field_name, field_def in schema_doc.schema['fields'].items():
            if field_def_param(field_def, 'type') in schema_doc.ns.types:
                nested_doc = getattr(schema_doc, field_name, None)
                if nested_doc is not None:
                    result.extend(self.failed_validation(nested_doc))

        return result

    def _collect_validation_rules(self, schema_doc: ISchemaDoc):
        """
        Collects validation rules for schema_doc and returns list of ISchemaDocValidationRule
        """
        rules = []

        for field_name, field_def in schema_doc.schema['fields'].items():
            validation = defaulted_field_def_param(field_def, 'validate')
            if validation == 'required':
                rules.append(FieldRequiredValidation(field_name=field_name, field_def=field_def))
            elif validation == 'not-empty':
                rules.append(FieldNotEmptyValidation(field_name=field_name, field_def=field_def))
            elif callable(validation):
                rules.append(CustomValidation(field_name=field_name, field_def=field_def))

        return rules


# ----------------------------------------------------------------------------------------------------------------------
# Описание несработавшей валидации
# ----------------------------------------------------------------------------------------------------------------------
class SchemaDocFailedValidation(ISchemaDocFailedValidation):
    """

    """
    def __init__(self, msg: str):
        self._msg = msg

    @property
    def msg(self) -> str:
        return self._msg


# ----------------------------------------------------------------------------------------------------------------------
# Правила валидации
# ----------------------------------------------------------------------------------------------------------------------
class FieldBasedSchemaDocValidationRule(ISchemaDocValidationRule):
    """ """

    def __init__(self, field_name: str, field_def: dict):
        self._field_def = field_def
        self._field_name = field_name

    @property
    def field_def(self) -> dict:
        return self._field_def

    @property
    def field_name(self) -> str:
        return self._field_name


class FieldRequiredValidation(FieldBasedSchemaDocValidationRule):
    """
    Правило валидации на то, что значение поля должно быть указано (любое значение, отличное от None)
    """

    def validate(self, doc: ISchemaDoc) -> Optional[ISchemaDocFailedValidation]:

        result = None
        if getattr(doc, self.field_name, None) is None:
            failed_msg = 'Не указано обязательное значение поля {0}'.format(self.field_name)
            result = SchemaDocFailedValidation(msg=failed_msg)

        return result


class FieldNotEmptyValidation(FieldBasedSchemaDocValidationRule):
    """
    Валидатор на то, что значение указано непустое (т.е., не None и не одно из значений, которые интепретируются
    системой как пустое)
    """
    def validate(self, doc: ISchemaDoc):

        # Сначала проверяем на то, что хотя бы какое-то значение было указано
        result = FieldRequiredValidation(field_name=self.field_name, field_def=self.field_def).validate(doc)
        if result:
            return result

        # Какое-то значение в поле указано, проверяем, что оно не соответствует "пустому" значению
        field_type = defaulted_field_def_param(self.field_def, 'type')
        field_value = getattr(doc, self.field_name, None)
        failed_msg = 'В поле {0} должно быть указано непустое значение'.format(self.field_name)

        if field_type in ('str', 'string', 'number', 'int', 'array', 'list', 'object', 'obj'):
            result = SchemaDocFailedValidation(msg=failed_msg) if not field_value else None
        elif field_type == 'date':
            result = SchemaDocFailedValidation(msg=failed_msg) if is_empty_date(field_value) else None
        elif field_type == 'datetime':
            result = SchemaDocFailedValidation(msg=failed_msg) if is_empty_datetime(field_value) else None
        elif field_type == 'uuid':
            result = SchemaDocFailedValidation(msg=failed_msg) if field_value == zero_uuid() else None

        # для bool/boolean не существует понятия "пустого значения" (только True и False)

        return result


class CustomValidation(FieldBasedSchemaDocValidationRule):

    def validate(self, doc: ISchemaDoc):
        """ Выполняем функцию валидации """
        result = None

        validate_cb = field_def_param(self.field_def, 'validate')

        if callable(validate_cb):
            field_value = getattr(doc, self.field_name, None)
            validate_cb_result = validate_cb(field_value, doc)

            result = SchemaDocFailedValidation(msg=validate_cb_result) if isinstance(validate_cb_result, str) else None

        return result
